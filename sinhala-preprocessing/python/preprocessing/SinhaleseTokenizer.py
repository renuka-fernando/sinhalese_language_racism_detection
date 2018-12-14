import re


def replace_url(text: str) -> str:
    return re.sub(r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)[a-z0-9]+([\-\.]{1}[a-z0-9A-Z\/]+)*', '', text)
