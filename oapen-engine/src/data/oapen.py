import logging
from typing import List

import requests
from model.oapen_types import (
    OapenItem,
    transform_item_data,
    transform_multiple_items_data,
)

SERVER_PATH = "https://library.oapen.org"
GET_COMMUNITY = "/rest/communities/{id}"
GET_COLLECTION = "/rest/collections/{id}"
GET_ITEM_BITSTREAMS = "/rest/items/{id}/bitstreams"
GET_COLLECTION_ITEMS = "/rest/collections/{id}/items"
GET_COMMUNITY_COLLECTIONS = "/rest/communities/{id}/collections"
GET_ITEM = "/rest/search?query=handle:%22{handle}%22&expand=bitstreams"
GET_COLLECTION_BY_LABEL = "/rest/search?query=oapen.collection:%22{label}%22"

# This is the only community we care about right now
BOOKS_COMMUNITY_ID = "3579505d-9d1b-4745-bcaf-a37329d25c69"


def get(endpoint, params=None):
    res = requests.get(url=SERVER_PATH + endpoint, params=params)
    if res.ok:
        if res.headers.get("content-type") == "application/json":
            return res.json()
        return res.content
    else:
        logging.error(str(res.status_code) + str(res.text))
        return None


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


def get_collection_items_by_id(id, limit=None) -> List[OapenItem]:
    res = get(endpoint=GET_COLLECTION_ITEMS.format(id=id), params={"limit": limit})

    if res is not None and len(res) > 0:
        return transform_multiple_items_data(res)
    return res


def get_collection_items_by_label(label, limit=None) -> List[OapenItem]:
    label = "+".join(label.split(" "))
    res = get(
        endpoint=GET_COLLECTION_BY_LABEL.format(label=label), params={"limit": limit}
    )

    if res is not None and len(res) > 0:
        return transform_multiple_items_data(res)
    return res


def get_bitstream_text(bitstreams, limit=None) -> str:
    for bitstream in bitstreams:
        if bitstream["mimeType"] == "text/plain":
            retrieveLink = bitstream["retrieveLink"]
            text = str(get(retrieveLink).decode("utf-8"))
            return text if limit is None else text[:limit]
    return ""
