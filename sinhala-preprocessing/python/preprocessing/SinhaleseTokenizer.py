import re


def replace_url(text: str) -> str:
    """
    replace URL of a text
    :param text: text to replace urls
    :return: url removed text
    """
    return re.sub(r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)[a-z0-9]+([\-\.]{1}[a-z0-9A-Z\/]+)*', '', text)


def remove_retweet_state(text: str) -> str:
    return re.sub(r'^RT @\w*:\ ', '', text)


txt = "RT @sam92ky: කියවන්න..රටේ දුප්පතාට @indika27 @P0dda මිනිස්සු කුණු දාන්නේ මූහූදට නෙ.,.... ඒකයි " \
      "මෙ https://t.co/xDrwvDa3yr ඔක්කොම https://t.co/xDrwvDa3yr case. Sighhhhhhhh  😢 " \
      "හස්බන්ඩ් උනත් එකයි නොවුනත් එකයි අපිට පුකද යාලුවේ.. 😜 #RT #Help"
print(remove_retweet_state(txt))
