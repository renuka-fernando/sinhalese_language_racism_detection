from SinhaleseVowelLetterFixer.SinhaleseCharacters import is_sinhalese_letter, is_sinhalese_vowel, get_fixed_vowel


class SinhaleseVowelLetterFixer:
    _fixed_text = ""
    _last_letter = ""
    _last_vowel = ""

    def __init__(self):
        self._clear()

    def _clear(self) -> None:
        self._fixed_text = ""
        self._last_letter = ""
        self._last_vowel = ""

    def get_fixed_text(self, text: str) -> str:
        for letter in text:
            if is_sinhalese_letter(letter):
                self._fixed_text += (self._last_letter + self._last_vowel)
                self._last_letter = letter
                self._last_vowel = ""
            elif is_sinhalese_vowel(letter):
                if self._last_letter == "":
                    print("Error : First letter can't be a vowel sign : " + letter)
                if self._last_vowel == "":
                    self._last_vowel = letter
                else:
                    try:
                        self._last_vowel = get_fixed_vowel(self._last_vowel + letter)
                    except KeyError:
                        # fix error of mistakenly duplicate vowel
                        if self._last_vowel == letter:
                            continue
                        else:
                            print("Error : can't fix vowe combination " + self._last_vowel + " + " + letter)
            else:
                self._fixed_text += (self._last_letter + self._last_vowel + letter)
                self._last_letter = ""
                self._last_vowel = ""

        return self._fixed_text
