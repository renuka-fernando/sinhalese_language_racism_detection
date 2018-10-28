import enum
import json
from string import Template

import requests
from requests_oauthlib import OAuth1


class TweeterPremiumAPI(enum.Enum):
    """
    Twitter API resource
    """
    day_30 = "30day"
    full_archive = "fullarchive"


def get_tweets_by_id(tweet_ids: list, oauth: OAuth1):
    """
    Get tweets of given list of user ids
    :param tweet_ids: list of tweet ids
    :param oauth: OAuth1 object for authentication
    :return: list of tweets
    """
    if len(tweet_ids) >= 100:
        raise ValueError("user id count = " + str(len(tweet_ids)) + ": user ids count should be 100 or less than 100")

    url = 'https://api.twitter.com/1.1/statuses/lookup.json?id=' + ','.join(tweet_ids)
    return json.loads(
        requests.get(
            url=url,
            auth=oauth
        ).text
    )


def search_tweets_standard_api(query: str, oauth: OAuth1) -> list:
    """
    retrieve tweets using standard API
    :param query: query to search
    :param oauth: OAuth1
    :return: tweets
    """
    # without "tweet_mode=extended"
    url_template = Template('https://api.twitter.com/1.1/search/tweets.json?q=$query&lang=si&count=15')
    return json.loads(
        requests.get(
            url=url_template.substitute(query=query),
            auth=oauth
        ).text
    )['statuses']


def search_tweets_premium_api(json_payload: json, oauth: OAuth1,
                              api: TweeterPremiumAPI = TweeterPremiumAPI.day_30) -> list:
    """
    retrieve tweets using premium API
    :param json_payload: Json Payload for the POST request
    :param oauth: OAuth1
    :param api: 30day or full_archive twitter API
    :return: tweets
    """
    url = "https://api.twitter.com/1.1/tweets/search/%s/dev.json" % api.value
    return json.loads(
        requests.post(
            url=url,
            json=json_payload,
            auth=oauth
        ).text
    )['results']


def fill_truncated_tweets(truncated_tweets: list, oauth: OAuth1) -> None:
    """
    fill truncated tweets with full tweet text
    :param truncated_tweets: list of truncated tweets
    :param oauth: OAuth1
    :return: tweets with full text
    """
    for i in range(0, len(truncated_tweets) // 100):
        full_tweets = get_tweets_by_id(tweet_ids=[tweet['id_str'] for tweet in truncated_tweets[i: 100 * (i + 1)]],
                                       oauth=oauth)
        for j in range(100):
            truncated_tweets[i * 100 + j]['text'] = full_tweets[j]['text']

    full_tweets = get_tweets_by_id(
        tweet_ids=[tweet['id_str'] for tweet in
                   truncated_tweets[len(truncated_tweets) // 100: len(truncated_tweets) % 100]],
        oauth=oauth)
    for j in range(len(truncated_tweets) % 100):
        truncated_tweets[len(truncated_tweets) // 100 + j]['text'] = full_tweets[j]
