sinhalese_chars = [
    "අ", "ආ", "ඇ", "ඈ", "ඉ", "ඊ",
    "උ", "ඌ", "ඍ", "ඎ", "ඏ", "ඐ",
    "එ", "ඒ", "ඓ", "ඔ", "ඕ", "ඖ",
    "ං", "ඃ",
    "ක", "ඛ", "ග", "ඝ", "ඞ", "ඟ",
    "ච", "ඡ", "ජ", "ඣ", "ඤ", "ඥ", "ඦ",
    "ට", "ඨ", "ඩ", "ඪ", "ණ", "ඬ",
    "ත", "ථ", "ද", "ධ", "න", "ඳ",
    "ප", "ඵ", "බ", "භ", "ම", "ඹ",
    "ය", "ර", "ල", "ව",
    "ශ", "ෂ", "ස", "හ", "ළ", "ෆ",
    "෴", "\u200d"
]
# "\u200d" is used with "යංශය" - කාව්‍ය, "රේඵය" - වර්‍තමාන, "Both" - මහාචාර්‍ය්‍ය, "රකාරාංශය" - මුද්‍රණය

sinhalese_vowel_signs = ["්", "ා", "ැ", "ෑ", "ි", "ී", "ු", "ූ", "ෘ", "ෙ", "ේ", "ෛ", "ො", "ෝ",
                         "ෞ", "ෟ", "ෲ", "ෳ", "ර්‍"]

# dictionary that maps wrong usage of vowels to correct vowels
vowel_sign_fix_dict = {
    "ෙ" + "්": "ේ",
    "්" + "ෙ": "ේ",

    "ෙ" + "ා": "ො",
    "ා" + "ෙ": "ො",

    "ේ" + "ා": "ෝ",
    "ො" + "්": "ෝ",

    "ෙෙ": "ෛ",
    "ෘෘ": "ෲ",

    "ෙ" + "ෟ": "ෞ",
    "ෟ" + "ෙ": "ෞ",

    "ි" + "ී": "ී",
    "ී" + "ි": "ී",

    # duplicating same symbol
    "ේ" + "්": "ේ",
    "ේ" + "ෙ": "ේ",

    "ො" + "ා": "ො",
    "ො" + "ෙ": "ො",

    "ෝ" + "ා": "ෝ",
    "ෝ" + "්": "ෝ",
    "ෝ" + "ෙ": "ෝ",
    "ෝ" + "ේ": "ෝ",
    "ෝ" + "ො": "ෝ",

    "ෞ" + "ෟ": "ෞ",
    "ෞ" + "ෙ": "ෞ",

    # special cases - may be typing mistakes
    "ො" + "ෟ": "ෞ",
    "ෟ" + "ො": "ෞ",
}

simplify_characters_dict = {
    # Consonant
    "ඛ": "ක",
    "ඝ": "ග",
    "ඟ": "ග",
    "ඡ": "ච",
    "ඣ": "ජ",
    "ඦ": "ජ",
    "ඤ": "ඥ",
    "ඨ": "ට",
    "ඪ": "ඩ",
    "ණ": "න",
    "ඳ": "ද",
    "ඵ": "ප",
    "භ": "බ",
    "ඹ": "බ",
    "ශ": "ෂ",
    "ළ": "ල",

    # Vowels
    "ආ": "අ",
    "ඈ": "ඇ",
    "ඊ": "ඉ",
    "ඌ": "උ",
    "ඒ": "එ",
    "ඕ": "ඔ",

    "ා": "",
    "ෑ": "ැ",
    "ී": "ි",
    "ූ": "ු",
    "ේ": "ෙ",
    "ෝ": "ො",
    "ෲ": "ෘ"
}


def is_sinhalese_letter(char: str) -> bool:
    return char in sinhalese_chars


def is_sinhalese_vowel(char: str) -> bool:
    return char in sinhalese_vowel_signs


def get_fixed_vowel(vowel: str) -> str:
    return vowel_sign_fix_dict[vowel]


def get_simplified_character(character: str) -> str:
    if len(character) != 1:
        raise TypeError("character should be a string with length 1")
    try:
        return simplify_characters_dict[character]
    except KeyError:
        return character
