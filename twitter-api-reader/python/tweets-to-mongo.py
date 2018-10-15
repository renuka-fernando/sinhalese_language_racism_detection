import json
from configparser import ConfigParser
from string import Template

import requests
from pymongo import MongoClient
from requests_oauthlib import OAuth1

config_parser = ConfigParser()
config_parser.read(filenames=['./config/twitter-keys.ini', './config/reader-config.ini'], encoding='utf-8')

url_template = Template('https://api.twitter.com/1.1/search/tweets.json?q=$query&lang=si&tweet_mode=extended')

# set OAuth with twitter configurations
oauth = OAuth1(
    client_key=config_parser.get('twitter', 'client_key'),
    client_secret=config_parser.get('twitter', 'client_secret'),
    resource_owner_key=config_parser.get('twitter', 'resource_owner_key'),
    resource_owner_secret=config_parser.get('twitter', 'resource_owner_secret')
)

url = url_template.substitute(query=config_parser.get('tweets', 'query'))
data = json.loads(requests.get(url, auth=oauth).text)

# Mongo Client
mongo_client = MongoClient(
    host=config_parser.get('mongo', 'host'),
    port=int(config_parser.get('mongo', 'port'))
)
# create tweets collection
tweets = mongo_client[config_parser.get('mongo', 'db')][config_parser.get('mongo', 'collection')]

for tweet in data['statuses']:
    tweets.insert_one(tweet)
