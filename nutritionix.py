import json
import requests
from urllib.parse import urljoin

BASE_URL = 'https://trackapi.nutritionix.com/v2/'

HEADER = {
    'X-APP-ID': 'd937c6fe',
    'X-APP-KEY': 'acdfb54f1c60e9ca2872badb7286ac8b',
}

def search(search_term): 
    """Perfrom a simple instant search on the nutrionix API"""

    params = {'query': search_term}

    endpoint = urljoin(BASE_URL, 'search/instant')

    r = requests.get(endpoint, params=params, headers=HEADER)

    resp = r.json()

    return resp

def search_item(item):
    """Performs a search to obtain nutrients of a specific item"""

    endpoint = urljoin(BASE_URL, 'search/item')

    params = {'nix_item_id': item}

    r = requests.get(endpoint, params=params, headers=HEADER)

    resp = r.json()

    return resp