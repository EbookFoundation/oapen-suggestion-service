import random
import time
from datetime import datetime
from typing import List, Iterable

import requests
from logger.base_logger import logger
from model.oapen_types import OapenItem
from data.oapen_oai import get_oapen_handles

SERVER_PATH = "https://library.oapen.org"
USER_AGENT = "oss_bot v0.0.1 <https://github.com/EbookFoundation/oapen_suggestion_service>"
GET_COLLECTIONS = "/rest/collections/"
GET_ITEM_BITSTREAMS = "/rest/items/{id}/bitstreams"
GET_COLLECTION_ITEMS = "/rest/collections/{id}/items"
GET_WEEKLY_ITEMS = "/rest/search?query=dc.date.accessioned_dt:[NOW-7DAY/DAY+TO+NOW]&expand=bitstreams,metadata"
GET_UPDATED_ITEMS = (
    "/rest/search?query=lastModified%3E{date}&expand=metadata,bitsteams"  # YYYY-MM-DD
)
GET_STREAM_QUERY = '/rest/search?query=handle:{handle}&expand=bitstreams'


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
]


def transform_item_data(item) -> OapenItem:
    thumbnail = get_bitstream_thumbnail(item)
    text = get_bitstream_text(item)
    return OapenItem(item["handle"], item["name"], thumbnail, text)


def oapen_item(handle) -> OapenItem:
    items =  get(
        endpoint=GET_STREAM_QUERY.format(handle=handle),
        params={"expand": "bitstreams"},
    )
    return transform_item_data(items)


def transform_multiple_items_data(items) -> List[OapenItem]:
    return [transform_item_data(item) for item in items]


def get(endpoint, params=None):

    res = requests.get(
        url=SERVER_PATH + endpoint,
        params=params,
        timeout=(None, 120),
        headers={"User-Agent": USER_AGENT},
    )

    ret = None
    if res.status_code == 200:
        if res.headers.get("content-type") == "application/json":
            ret = res.json()
        else:
            ret = res.content
    else:
        logger.error("ERROR - GET {}: {}".format(res.url, res.status_code))
        logger.debug("GET {}: {}".format(res.url, res.status_code))
    return ret


def get_all_collections():
    res = get(endpoint=GET_COLLECTIONS)
    return res


def get_collection_items_by_endpoint(endpoint) -> List[OapenItem]:
    res = get(endpoint=endpoint)

    if res is not None and len(res) > 0:
        return transform_multiple_items_data(res)
    return res


# Gets all items added in the last week
def get_weekly_items(limit=None) -> Iterable[OapenItem]:
    num = 0
    for handle, item_type in get_oapen_handles(from_date='week'):
        if limit and num > limit:
            return
 
        endpoint = GET_STREAM_QUERY.format(handle=handle)
        res = get(endpoint=endpoint)
        if res is not None and len(res) > 0:
            num += 1
            yield transform_item_data(res[0])


def get_updated_items(date: datetime, limit=None, offset=None) -> List[OapenItem]:
    date = date.strftime("%Y-%m-%d")
    res = get(
        endpoint=GET_UPDATED_ITEMS.format(date=date),
        params={"limit": limit, "offset": offset},
    )

    if res is not None and len(res) > 0:
        return transform_multiple_items_data(res)
    return res


# General function to extract the retrieveLink of a bitstream with type bitstream_type
def __get_bitstream_url(bitstreams, bundle_name: str) -> str or None:
    if bitstreams is not None:
        for bitstream in bitstreams:
            if bitstream["bundleName"] == bundle_name:
                return bitstream["retrieveLink"]
    return None


# limit: int - number of characters
def get_bitstream_text(item) -> str:
    retrieveLink = __get_bitstream_url(item["bitstreams"], "TEXT")
    if retrieveLink is not None:
        time.sleep(1)  # Attempt to avoid rate limiting
        text = str(get(retrieveLink).decode("utf-8"))
        return text
    else:
        return ""


def get_bitstream_thumbnail(item):
    return __get_bitstream_url(item["bitstreams"], "THUMBNAIL")
