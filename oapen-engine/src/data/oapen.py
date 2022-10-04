import requests
import json
from xml.etree import ElementTree

SERVER_PATH = "https://library.oapen.org/rest"
GET_COMMUNITY = "/communities/"
GET_COLLECTION = "/collections/"
GET_BITSTREAM = "/search"
GET_COLLECTION_ITEMS = "/collections/{id}/items"
GET_COMMUNITY_COLLECTIONS = "/communities/{id}/collections"

# This is the onl
BOOKS_COMMUNITY_ID = "3579505d-9d1b-4745-bcaf-a37329d25c69"

def send_get_request(endpoint, params = None):
    req = requests.get(url = SERVER_PATH + endpoint, params=params)
    return req.json()

def get_all_communities():
    return send_get_request(endpoint=GET_COMMUNITY)

def get_community(community):
    return send_get_request(endpoint=GET_COMMUNITY + community)

def get_collection(collection):
    return send_get_request(endpoint=GET_COLLECTION + collection)

def get_bitstream(handle):
    params = {
        "query": "handle:%22" + str(handle) + "%22",
        "expand":"bitstreams"
    }
    return send_get_request(endpoint=GET_BITSTREAM, params=params)


def get_collections_from_community(community):
    data = send_get_request(endpoint=GET_COMMUNITY_COLLECTIONS.format(id=community))
    return [x['uuid'] for x in data]

def get_items_from_collection(collection):
    data = send_get_request(endpoint=GET_COLLECTION_ITEMS.format(id=collection))
    return [x['uuid'] for x in data]
    
