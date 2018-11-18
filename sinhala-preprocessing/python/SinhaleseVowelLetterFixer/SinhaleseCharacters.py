sinhalese_chars = [
    "අ", "ආ", "ඇ", "ඈ", "ඉ", "ඊ",
    "උ", "ඌ", "ඍ", "ඎ", "ඏ", "ඐ",
    "එ", "ඒ", "ඓ", "ඔ", "ඕ", "ඖ",
    "ං", "ඃ"
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


def is_sinhalese_letter(char: str) -> bool:
    return char in sinhalese_chars


def is_sinhalese_vowel(char: str) -> bool:
    return char in sinhalese_vowel_signs


def get_fixed_vowel(vowel: str) -> str:
    return vowel_sign_fix_dict[vowel]
