import json
from configparser import ConfigParser

import requests
from requests_oauthlib import OAuth1

config = ConfigParser()
config.read('./config/reader-config.ini')

CLIENT_KEY = config.get('twitter', 'client_key')
CLIENT_SECRET = config.get('twitter', 'client_secret')
RESOURCE_OWNER_KEY = config.get('twitter', 'resource_owner_key')
RESOURCE_OWNER_SECRET = config.get('twitter', 'resource_owner_secret')

oauth = OAuth1(client_key=CLIENT_KEY,
               client_secret=CLIENT_SECRET,
               resource_owner_key=RESOURCE_OWNER_KEY,
               resource_owner_secret=RESOURCE_OWNER_SECRET)

url = 'https://api.twitter.com/1.1/search/tweets.json?q=මම&lang=si'
data = json.loads(requests.get(url, auth=oauth).text)
