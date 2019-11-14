import json
import requests
from urllib.parse import urljoin
import config

BASE_URL = 'https://trackapi.nutritionix.com/v2/'

HEADER = {
    'X-APP-ID': config.X_APP_ID,
    'X-APP-KEY': config.X_APP_KEY,
}

def search(search_term): 
    """Perfrom a simple instant search on the nutrionix API"""

    params = {'query': search_term, 'detailed': 'True'}

    endpoint = urljoin(BASE_URL, 'search/instant')

    r = requests.get(endpoint, params=params, headers=HEADER)

    resp = r.json()

    return resp  

def search_branded_item(item):
    """Performs a search to obtain nutrients of a branded food item,
    given its NIX item ID"""

    endpoint = urljoin(BASE_URL, 'search/item')

    params = {'nix_item_id': item}

    r = requests.get(endpoint, params=params, headers=HEADER)

    resp = r.json()

    food_info = resp['foods'][0]

    return food_info