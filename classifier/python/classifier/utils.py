import os

import numpy as np

from classifier.data_set_constants import DATA_SET_CLASSES
from preprocessing.sinhalese_tokenizer import tokenize


def tokenize_corpus(corpus: list) -> list:
    return [tokenize(text) for text in corpus]


def transform_class_to_one_hot_representation(classes: list):
    return np.array([DATA_SET_CLASSES[cls] for cls in classes])


def build_dictionary(corpus_token: list) -> dict:
    word_frequency = {}
    dictionary = {}

    for tweet in corpus_token:
        for token in tweet:
            if token in word_frequency:
                word_frequency[token] += 1
            else:
                word_frequency[token] = 1

    frequencies = list(word_frequency.values())
    unique_words = list(word_frequency.keys())

    # sort words by its frequency
    frequency_indexes = np.argsort(frequencies)[::-1]  # reverse for descending
    for index, frequency_index in enumerate(frequency_indexes):
        # 0 is not used and 1 is for UNKNOWN
        dictionary[unique_words[frequency_index]] = index + 2

    return dictionary


def transform_to_dictionary_values(corpus_token: list, dictionary: dict) -> list:
    x_corpus = []
    for tweet in corpus_token:
        # 1 is for unknown (not in dictionary)
        x_corpus.append([dictionary[token] if token in dictionary else 1 for token in tweet])

    return x_corpus


def get_calculated_user_profile(user_ids: list, classes: list) -> dict:
    user_profile = {}
    user_tweets_count = {}

    for i in range(len(user_ids)):
        # count tweets with class
        try:
            user_profile[user_ids[i], classes[i]] += 1
        except KeyError:
            user_profile[user_ids[i], classes[i]] = 1

        # count tweets
        try:
            user_tweets_count[user_ids[i]] += 1
        except KeyError:
            user_tweets_count[user_ids[i]] = 1

    # calculate mean
    for profile in user_profile.keys():
        user_profile[profile] /= user_tweets_count[profile[0]]

    return user_profile


def append_user_profile_features(x_corpus: list, user_ids: list, user_profile: dict) -> list:
    """
    append neutral, racism, sexism user profile probability feature to the end of each sentence
    :param x_corpus: corpus with coded to integers
    :param user_ids: list of user ids in the order of x_corpus
    :param user_profile: user profile with user's probabilities for neutral, racism, sexism
    :return: appended x_corpus
    """
    for i in range(len(x_corpus)):
        uid = user_ids[i]
        try:
            neutral = user_profile[uid, "Neutral"]
        except KeyError:
            neutral = 0

        try:
            racism = user_profile[uid, "Racist"]
        except KeyError:
            racism = 0

        try:
            sexism = user_profile[uid, "Sexism"]
        except KeyError:
            sexism = 0

        x_corpus[i].append(int(neutral * 1000))
        x_corpus[i].append(int(racism * 1000))
        x_corpus[i].append(int(sexism * 1000))

    return x_corpus


def create_next_results_folder():
    """
    Create the next results folder and returns the directory name
    :return: directory name
    """
    result_no = 0
    directory = "results_%d" % result_no

    while os.path.exists(directory):
        result_no += 1
        directory = "results_%d" % result_no

    os.makedirs(directory)
    return directory


def get_last_results_folder():
    """
    Return last created results directory
    :return: last created results directory
    """
    result_no = 0
    directory = "results_%d" % result_no

    while os.path.exists(directory):
        result_no += 1
        directory = "results_%d" % result_no

    return "results_%d" % (result_no - 1)
