from datetime import datetime
from typing import List

import requests
from model.oapen_types import OapenItem, transform_item_data

SERVER_PATH = "https://library.oapen.org"
GET_COMMUNITY = "/rest/communities/{id}"
GET_COLLECTION = "/rest/collections/{id}"
GET_COLLECTIONS = "/rest/collections/"
GET_ITEM_BITSTREAMS = "/rest/items/{id}/bitstreams"
GET_COLLECTION_ITEMS = "/rest/collections/{id}/items"
GET_COMMUNITY_COLLECTIONS = "/rest/communities/{id}/collections"
GET_ITEM = "/rest/search?query=handle:%22{handle}%22&expand=bitstreams,metadata"
GET_COLLECTION_BY_LABEL = (
    "/rest/search?query=oapen.collection:%22{label}%22&expand=metadata"
)

GET_WEEKLY_ITEMS = "/rest/search?query=dc.date.accessioned_dt:[NOW-7DAY/DAY+TO+NOW]&expand=bitstreams,metadata"
GET_UPDATED_ITEMS = (
    "/rest/search?query=lastModified%3E{date}&expand=metadata,bitsteams"  # YYYY-MM-DD
)

# This is the only community we care about right now
BOOKS_COMMUNITY_ID = "3579505d-9d1b-4745-bcaf-a37329d25c69"


def transform_multiple_items_data(items) -> List[OapenItem]:
    return [
        transform_item_data(item, get_bitstream_text(item["bitstreams"]))
        for item in items
    ]


def get(endpoint, params=None, log=False):
    res = requests.get(url=SERVER_PATH + endpoint, params=params, timeout=(None, 120))

    ret = None
    if res.status_code == 200:
        if res.headers.get("content-type") == "application/json":
            ret = res.json()
        else:
            ret = res.content
    else:
        print("GET {}: {}".format(res.url, res.status_code))

    if log:
        print("GET {}: {}".format(res.url, res.status_code))
    return ret


def get_all_communities():
    return get(endpoint=GET_COMMUNITY)


def get_community(id):
    return get(endpoint=GET_COMMUNITY.format(id=id))


def get_collection(id):
    return get(endpoint=GET_COLLECTION.format(id=id))


def get_item(handle) -> OapenItem:
    res = get(endpoint=GET_ITEM.format(handle=handle))

    if res is not None and len(res) > 0:
        return transform_item_data(res[0], get_bitstream_text(res[0]["bitstreams"]))
    return res


def get_collections_from_community(id):
    res = get(endpoint=GET_COMMUNITY_COLLECTIONS.format(id=id))
    return res


def get_all_collections():
    res = get(endpoint=GET_COLLECTIONS, log=True)
    return res


def get_collection_items_by_id(id, limit=None, offset=None) -> List[OapenItem]:
    res = get(
        endpoint=GET_COLLECTION_ITEMS.format(id=id),
        params={"expand": "bitstreams,metadata", "limit": limit, "offset": offset},
        log=True,
    )

    if res is not None and len(res) > 0:
        return transform_multiple_items_data(res)
    return res


def get_collection_items_by_label(label, limit=None) -> List[OapenItem]:
    label = "+".join(label.split(" "))
    res = get(
        endpoint=GET_COLLECTION_BY_LABEL.format(label=label),
        params={"limit": limit},
        log=True,
    )

    if res is not None and len(res) > 0:
        return transform_multiple_items_data(res)
    return res


def get_bitstream_text(bitstreams, limit=None) -> str:
    if bitstreams is not None:
        for bitstream in bitstreams:
            if bitstream["mimeType"] == "text/plain":
                retrieveLink = bitstream["retrieveLink"]
                text = str(get(retrieveLink).decode("utf-8"))
                return text if limit is None else text[:limit]
    return ""


# Gets all items added in the last week
def get_weekly_items(limit=None) -> List[OapenItem]:
    res = get(endpoint=GET_WEEKLY_ITEMS, params={"limit": limit})

    if res is not None and len(res) > 0:
        return transform_multiple_items_data(res)
    return res


def get_updated_items(date: datetime, limit=None, offset=None) -> List[OapenItem]:

    date = date.strftime("%Y-%m-%d")
    res = get(
        endpoint=GET_UPDATED_ITEMS.format(date=date),
        params={"limit": limit, "offset": offset},
    )

    if res is not None and len(res) > 0:
        return transform_multiple_items_data(res)
    return res
