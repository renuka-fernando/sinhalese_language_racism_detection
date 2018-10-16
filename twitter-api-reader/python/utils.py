import json
from string import Template

import requests
from requests_oauthlib import OAuth1


def get_tweets_of_users(user_ids: list, oauth: OAuth1):
    """
    Get tweets of given list of user ids
    :param user_ids: list of user ids
    :param oauth: OAuth1 object for authentication
    :return: list of tweets
    """
    if len(user_ids) >= 100:
        raise ValueError("user id count = " + str(len(user_ids)) + ": user ids count should be 100 or less than 100")

    url = 'https://api.twitter.com/1.1/statuses/lookup.json?id=' + ','.join(str(user_id) for user_id in user_ids)
    return json.loads(
        requests.get(
            url=url,
            auth=oauth
        ).text
    )


def search_tweets_standard_api(query: str, oauth: OAuth1):
    url_template = Template('https://api.twitter.com/1.1/search/tweets.json?q=$query&lang=si&tweet_mode=extended')
    return json.loads(
        requests.get(
            url=url_template.substitute(query=query),
            auth=oauth
        ).text
    )['statuses']


def search_tweets_premium_api(json_payload: json, oauth: OAuth1):
    url = 'https://api.twitter.com/1.1/tweets/search/30day/dev.json'
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
        full_tweets = get_tweets_of_users(user_ids=[user_id for user_id in truncated_tweets[i: 100 * (i + 1)]],
                                          oauth=oauth)
        for j in range(100):
            truncated_tweets[i * 100 + j]['text'] = full_tweets[j]['text']

    full_tweets = get_tweets_of_users(
        user_ids=[user_id for user_id in truncated_tweets[len(truncated_tweets) // 100: len(truncated_tweets) % 100]],
        oauth=oauth)
    for j in range(len(truncated_tweets) % 100):
        truncated_tweets[len(truncated_tweets) // 100 + j]['text'] = full_tweets[j]
