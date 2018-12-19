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
