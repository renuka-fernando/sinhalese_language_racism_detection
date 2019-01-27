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


class TweetQueryError(Exception):
    pass


def get_tweets_by_id(tweet_ids: list, oauth: OAuth1):
    """
    Get tweets of given list of tweet ids
    :param tweet_ids: list of tweet ids
    :param oauth: OAuth1 object for authentication
    :return: list of tweets
    """
    if len(tweet_ids) >= 100:
        raise ValueError("user id count = " + str(len(tweet_ids)) + ": user ids count should be 100 or less than 100")

    url = 'https://api.twitter.com/1.1/statuses/lookup.json?tweet_mode=extended&id=' + ','.join(tweet_ids)
    return json.loads(
        requests.get(
            url=url,
            auth=oauth
        ).text
    )


def get_tweets_by_user_id(user_id: str, oauth: OAuth1) -> list:
    """
    Get tweets of given user id
    :param user_id: user id
    :param oauth: OAuth1 object for authentication
    :return: list of tweets
    """
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?count=200&user_id=' + user_id
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
    url_template = Template('https://api.twitter.com/1.1/search/tweets.json?q=$query&lang=si&count=100')
    data = json.loads(requests.get(
        url=url_template.substitute(query=query + ' -RT'),
        auth=oauth
    ).text)
    try:
        return data['statuses']
    except KeyError:
        raise TweetQueryError(" AND ".join([err['message'] for err in data['errors']]))


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
    data = json.loads(requests.post(
        url=url,
        json=json_payload,
        auth=oauth
    ).text)
    try:
        return data['results']
    except KeyError:
        raise TweetQueryError(data['error']['message'])


def _set_full_tweet_text(truncated_tweets: list, full_tweets: list) -> None:
    # have to search the tweet because the response is not in the order of the requested tweet ids
    for truncated_tweet in truncated_tweets:
        for full_tweet in full_tweets:
            if truncated_tweet['id'] == full_tweet['id']:
                truncated_tweet['text'] = full_tweet['full_text']
                break
        else:
            print("Full tweet did not found for the truncated tweet (id): " + truncated_tweet['id_str'])


def fill_truncated_tweets(truncated_tweets: list, oauth: OAuth1) -> None:
    """
    fill truncated tweets with full tweet text
    :param truncated_tweets: list of truncated tweets
    :param oauth: OAuth1
    :return: tweets with full text
    """
    for i in range(0, len(truncated_tweets) // 100):
        full_tweets = get_tweets_by_id(
            tweet_ids=[tweet['id_str'] for tweet in truncated_tweets[100 * i: 100 * (i + 1)]],
            oauth=oauth)
        # fill truncated tweets
        _set_full_tweet_text(truncated_tweets[100 * i: 100 * (i + 1)], full_tweets)

    full_tweets = get_tweets_by_id(
        tweet_ids=[tweet['id_str'] for tweet in truncated_tweets[-(len(truncated_tweets) % 100):]], oauth=oauth)
    # fill truncated tweets
    _set_full_tweet_text(truncated_tweets[-(len(truncated_tweets) % 100):], full_tweets)
