import requests
import json

COMMUNITY_URL = "https://library.oapen.org/rest/communities/"
COLLECTION_URL = "https://library.oapen.org/rest/collections/"
BITSTREAM_URL = "https://library.oapen.org/rest/search"

def send_get_request(url, params = None):
    req = requests.get(url = url, params=params)
    res = req.json()
    return json.load(res)

def get_all_communities():
    send_get_request(url=COMMUNITY_URL)

def get_community(community):
    send_get_request(url=COMMUNITY_URL + community)

def get_collection(collection):
    send_get_request(url=COLLECTION_URL + collection)

def get_bitstream(handle):
    params = {
        "query": "handle:%22" + str(handle) + "%22",
        "expand":"bitstreams"
    }
    send_get_request(url=BITSTREAM_URL, params=params)