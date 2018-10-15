import json
from configparser import ConfigParser

import requests
from pymongo import MongoClient
from requests_oauthlib import OAuth1

config_parser = ConfigParser()
config_parser.read(filenames=['./config/twitter-keys.ini', './config/reader-config.ini'], encoding='utf-8')

# set OAuth with twitter configurations
oauth = OAuth1(
    client_key=config_parser.get('twitter', 'client_key'),
    client_secret=config_parser.get('twitter', 'client_secret'),
    resource_owner_key=config_parser.get('twitter', 'resource_owner_key'),
    resource_owner_secret=config_parser.get('twitter', 'resource_owner_secret')
)


def search_tweets_premium_api():
    url = 'https://api.twitter.com/1.1/tweets/search/30day/dev.json'
    return json.loads(
        requests.post(
            url=url,
            json=json.loads(config_parser.get('tweets', 'json_payload')),
            auth=oauth
        ).text
    )


def get_tweet(id):
    url = 'https://api.twitter.com/1.1/statuses/lookup.json?id=' + str(id)
    return json.loads(
        requests.get(
            url=url,
            auth=oauth
        ).text
    )


data = search_tweets_premium_api()

# Mongo Client
mongo_client = MongoClient(
    host=config_parser.get('mongo', 'host'),
    port=int(config_parser.get('mongo', 'port'))
)
# create tweets collection
tweets = mongo_client[config_parser.get('mongo', 'db')][config_parser.get('mongo', 'collection')]

for tweet in data['results']:
    if tweet['truncated']:
        text = get_tweet(tweet['id'])[0]['text']
        tweet['text'] = text
    tweets.insert_one(tweet)
