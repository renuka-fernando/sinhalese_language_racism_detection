import re

import emoji

from preprocessing.sinhalese_characters import get_simplified_character


def replace_url(text: str) -> str:
    """
    replace URL of a text
    :param text: text to replace urls
    :return: url removed text
    """
    return re.sub(r'(http://www\.|https://www\.|http://|https://)[a-z0-9]+([\-.]{1}[a-z0-9A-Z/]+)*', '', text)


def remove_retweet_state(text: str) -> str:
    """
    remove retweet states in the beginning such as "RT @sam92ky: "
    :param text: text
    :return: text removed retweets state
    """
    return re.sub(r'^RT @\w*: ', '', text)


def replace_mention(text: str) -> str:
    return re.sub(r'@\w*', 'PERSON', text)


def split_tokens(text: str) -> list:
    """
    tokenize text
    :param text: text
    :return: token list
    """
    # text characters to split is from: https://github.com/madurangasiriwardena/corpus.sinhala.tools
    emojis = ''.join(emj for emj in emoji.UNICODE_EMOJI.keys())
    return [token for token in
            re.split(r'[.…,‌ ¸‚\"/|—¦”‘\'“’´!@#$%^&*+\-£?˜()\[\]{\}:;–Ê  �‪‬‏0123456789' + emojis + ']', text)
            if token != ""]


def set_spaces_among_emojis(text: str) -> str:
    """
    make spaces among emojis to tokenize them
    :param text: text to be modified
    :return: modified text
    """
    modified_text = ""
    for c in text:
        modified_text += c
        if c in emoji.UNICODE_EMOJI:
            modified_text += " "

    return modified_text


def simplify_sinhalese_text(text: str) -> str:
    """
    simplify
    :param text:
    :return:
    """
    modified_text = ""
    for c in text:
        modified_text += get_simplified_character(c)
    return modified_text


def stem_word(word: str) -> str:
    """
    Stemming words
    :param word: word
    :return: stemmed word
    """
    if len(word) < 4:
        return word

    # remove 'ට'
    if word[-1] == 'ට':
        return word[:-1]

    # remove 'ද'
    if word[-1] == 'ද':
        return word[:-1]

    # remove 'ටත්'
    if word[-3:] == 'ටත්':
        return word[:-3]

    # remove 'එක්'
    if word[-3:] == 'ෙක්':
        return word[:-3]

    # remove 'එ'
    if word[-1:] == 'ෙ':
        return word[:-1]

    # remove 'ක්'
    if word[-2:] == 'ක්':
        return word[:-2]

    # remove 'ගෙ' (instead of ගේ because this step comes after simplifying text)
    if word[-2:] == 'ගෙ':
        return word[:-2]

    # else
    return word


def tokenize(text: str) -> list:
    # todo: add stem_word(token) and simplify_sinhalese_text methods
    return [stem_word(token) for token in split_tokens(replace_url(replace_mention(
        simplify_sinhalese_text(remove_retweet_state(text.strip('"')).lower()))))]

