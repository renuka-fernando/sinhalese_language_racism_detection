from configparser import ConfigParser

from pymongo import MongoClient
from requests_oauthlib import OAuth1

import utils

config_parser = ConfigParser()
config_parser.read(filenames=['./config/twitter-keys.ini', './config/reader-config.ini'], encoding='utf-8')

# set OAuth with twitter configurations
oauth = OAuth1(client_key=config_parser.get('twitter', 'client_key'),
               client_secret=config_parser.get('twitter', 'client_secret'),
               resource_owner_key=config_parser.get('twitter', 'resource_owner_key'),
               resource_owner_secret=config_parser.get('twitter', 'resource_owner_secret'))

data = utils.search_tweets_standard_api(query=config_parser.get('tweets', 'query'),
                                        oauth=oauth)

# Mongo Client
mongo_client = MongoClient(host=config_parser.get('mongo', 'host'),
                           port=int(config_parser.get('mongo', 'port')))
# create tweets collection
tweets_mongo_collection = mongo_client[config_parser.get('mongo', 'db')][config_parser.get('mongo', 'collection')]

truncated_tweets = []
for tweet in data:
    if tweet['truncated']:
        truncated_tweets.append(tweet)
    else:
        tweets_mongo_collection.insert_one(tweet)

# fill truncated text field of tweets
utils.fill_truncated_tweets(truncated_tweets, oauth)
if len(truncated_tweets) != 0:
    tweets_mongo_collection.insert_many(truncated_tweets)
