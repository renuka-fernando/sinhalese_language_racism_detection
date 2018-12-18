from preprocessing.sinhalese_characters import get_fixed_vowel, is_sinhalese_vowel, is_sinhalese_letter


class SinhaleseVowelLetterFixer:
    """
    Sinhalese Language Vowel Letter Fixer
    """

    @staticmethod
    def get_fixed_text(text: str) -> str:
        """
        Fix wrong usage of vowels
        :param text: text to be fixed
        :return: fixed text with proper vowels
        """
        fixed_text = ""
        last_letter = ""
        last_vowel = ""

        for letter in text:
            if is_sinhalese_letter(letter):
                fixed_text += (last_letter + last_vowel)
                last_letter = letter
                last_vowel = ""
            elif is_sinhalese_vowel(letter):
                if last_letter == "":
                    print("Error : First letter can't be a vowel sign : " + letter)
                if last_vowel == "":
                    last_vowel = letter
                else:
                    try:
                        last_vowel = get_fixed_vowel(last_vowel + letter)
                    except KeyError:
                        # fix error of mistakenly duplicate vowel
                        if last_vowel == letter:
                            continue
                        else:
                            print("Error : can't fix vowel combination " + last_vowel + " + " + letter)
            else:
                fixed_text += (last_letter + last_vowel + letter)
                last_letter = ""
                last_vowel = ""

        fixed_text += last_letter + last_vowel
        return fixed_text


# Test
wrong_text = "ද" + "ෙ" + "ෙ" + "ව" + "ය"
correct_text = "ද" + "ෛ" + "ව" + "ය"
corrected_text = SinhaleseVowelLetterFixer.get_fixed_text(wrong_text)
assert correct_text == corrected_text
