import requests

SERVER_PATH = "https://library.oapen.org"
GET_COMMUNITY = "/rest/communities/{id}"
GET_COLLECTION = "/rest/collections/{id}"
GET_ITEM_BITSTREAMS = "/rest/items/{id}/bitstreams"
GET_COLLECTION_ITEMS = "/rest/collections/{id}/items"
GET_COMMUNITY_COLLECTIONS = "/rest/communities/{id}/collections"
GET_ITEM = "/rest/items/{id}"

# This is the only community we care about right now
BOOKS_COMMUNITY_ID = "3579505d-9d1b-4745-bcaf-a37329d25c69"


def get(endpoint, params=None):
    res = requests.get(url=SERVER_PATH + endpoint, params=params)
    if res.ok:
        if res.headers.get("content-type") == "application/json":
            return res.json()
        return res.content
    else:
        return str(res.status_code) + str(res.text)


def get_all_communities():
    return get(endpoint=GET_COMMUNITY)


def get_community(community):
    return get(endpoint=GET_COMMUNITY.format(id=community))


def get_collection(collection):
    return get(endpoint=GET_COLLECTION.format(id=collection))


def get_item(item):
    return get(endpoint=GET_ITEM.format(id=item))


def get_bitstreams(item):
    return get(endpoint=GET_ITEM_BITSTREAMS.format(id=item))


def get_collections_from_community(community):
    data = get(endpoint=GET_COMMUNITY_COLLECTIONS.format(id=community))
    return [x["uuid"] for x in data]


def get_items_from_collection(collection):
    data = get(endpoint=GET_COLLECTION_ITEMS.format(id=collection))
    return [x["uuid"] for x in data]
