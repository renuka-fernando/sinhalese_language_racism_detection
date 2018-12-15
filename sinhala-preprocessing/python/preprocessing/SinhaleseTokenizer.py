import re

import emoji


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


def replace_mension(text: str) -> str:
    return re.sub(r'@\w*', 'PERSON', text)


def split_tokens(text: str) -> list:
    """
    tokenize text
    :param text: text
    :return: token list
    """
    # text characters to split is from: https://github.com/madurangasiriwardena/corpus.sinhala.tools
    return [token for token in
            re.split(r'[., ¸‚\"/|—¦”‘\'“’´!@#$%^&*+\-£?˜()\[\]{\}:;–Ê  �‪‬‏0123456789]', text) if
            token != ""]


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


txt = "RT @sam92ky: කියවන්න..රටේ Renuka දුප්පතාට @indika27 @P0dda මිනිස්සු කුණු දාන්නේ මූහූදට නෙ.,.... ඒකයි " \
      "මෙ https://t.co/xDrwvDa3yr ඔක්කොම https://t.co/xDrwvDa3yr case. Sighhhhhhhh  😢 " \
      "හස්බන්ඩ් උනත් {එකයි}***-+නොවුනත් [එකයි අපිට] සෝන්ග් 😂😂😂🌺 පුකද යාලුවේ.. 😜 #RT #Help"
print(split_tokens(set_spaces_among_emojis(replace_url(replace_mension(remove_retweet_state(txt))))))
