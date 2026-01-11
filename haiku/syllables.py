import re

import cmudict

CMU_DICT = cmudict.dict()

ONES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
TEENS = [
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def number_to_words(n: int) -> str:
    if n < 0:
        return "negative " + number_to_words(-n)
    if n == 0:
        return "zero"
    if n < 10:
        return ONES[n]
    if n < 20:
        return TEENS[n - 10]
    if n < 100:
        return TENS[n // 10] + (" " + ONES[n % 10] if n % 10 else "")
    if n < 1000:
        return ONES[n // 100] + " hundred" + (" " + number_to_words(n % 100) if n % 100 else "")
    if n < 1000000:
        remainder = " " + number_to_words(n % 1000) if n % 1000 else ""
        return number_to_words(n // 1000) + " thousand" + remainder
    return " ".join(number_to_words(int(d)) for d in str(n) if d != "0")


def count_syllables_word(word: str) -> int:
    word = re.sub(r"[^a-zA-Z0-9]", "", word).lower()
    if not word:
        return 0
    if word.isdigit():
        return count_syllables(number_to_words(int(word)))
    phones = CMU_DICT.get(word)
    if phones:
        return sum(1 for p in phones[0] if p[-1].isdigit())
    vowels = len(re.findall(r"[aeiouy]+", word))
    return max(vowels, 1)


def count_syllables(text: str) -> int:
    return sum(count_syllables_word(word) for word in text.split())
