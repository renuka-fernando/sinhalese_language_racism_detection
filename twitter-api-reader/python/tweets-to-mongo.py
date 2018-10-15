import json
from configparser import ConfigParser

import requests
from pymongo import MongoClient
from requests_oauthlib import OAuth1

config = ConfigParser()
config.read('./config/reader-config.ini')

# set OAuth with twitter configurations
oauth = OAuth1(client_key=config.get('twitter', 'client_key'),
               client_secret=config.get('twitter', 'client_secret'),
               resource_owner_key=config.get('twitter', 'resource_owner_key'),
               resource_owner_secret=config.get('twitter', 'resource_owner_secret'))

url = 'https://api.twitter.com/1.1/search/tweets.json?q=මම&lang=si'
data = json.loads(requests.get(url, auth=oauth).text)

# Mongo Client, create tweets collection
mongo_client = MongoClient(config.get('mongo', 'host'), int(config.get('mongo', 'port')))
tweets = mongo_client.db.tweets

for tweet in data['statuses']:
    tweets.insert_one(tweet)
