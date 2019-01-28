import sys
from configparser import ConfigParser

from pandas import json
from pymongo import MongoClient
from requests_oauthlib import OAuth1

sys.path.append("../")
from twitter import utils

config_parser = ConfigParser()
config_parser.read(filenames=['../config/twitter-keys.ini', '../config/reader-config.ini'], encoding='utf-8')

# set OAuth with twitter configurations
oauth = OAuth1(client_key=config_parser.get('twitter', 'client_key'),
               client_secret=config_parser.get('twitter', 'client_secret'),
               resource_owner_key=config_parser.get('twitter', 'resource_owner_key'),
               resource_owner_secret=config_parser.get('twitter', 'resource_owner_secret'))

# read twitter API
api_type = "s"  # s: Standard, p30: Premium 30 days, pf: Premium Full Archive
if len(sys.argv) > 1:
    option = sys.argv[1]
    if option in ['s', 'p30', 'pf']:
        api_type = option
    else:
        raise ValueError("First argument should be API type: s or p30 or pf")

if api_type == 's':
    # ##### Standard API #####
    data = utils.search_tweets_standard_api(query=config_parser.get('tweets', 'query'),
                                            oauth=oauth)
elif api_type == 'p30':
    # ##### Premium API 30 days #####
    data = utils.search_tweets_premium_api(json_payload=json.loads(config_parser.get('tweets', 'json_payload')),
                                           api=utils.TweeterPremiumAPI.day_30,
                                           oauth=oauth)
elif api_type == 'pf':
    # ##### Premium API Full Archive #####
    data = utils.search_tweets_premium_api(json_payload=json.loads(config_parser.get('tweets', 'json_payload')),
                                           api=utils.TweeterPremiumAPI.full_archive,
                                           oauth=oauth)
else:
    assert False, 'First argument should be API type: s or p30 or pf'

# ##### Get tweets by user id #####
# data = utils.get_tweets_by_user_id("1219328588", oauth)

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
