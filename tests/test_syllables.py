from haiku.syllables import count_syllables, count_syllables_word


def test_simple_words():
    assert count_syllables_word("hello") == 2
    assert count_syllables_word("world") == 1
    assert count_syllables_word("beautiful") == 3


def test_single_syllable():
    assert count_syllables_word("cat") == 1
    assert count_syllables_word("the") == 1
    assert count_syllables_word("I") == 1


def test_numbers():
    assert count_syllables_word("3") == 1  # three
    assert count_syllables_word("7") == 2  # sev-en
    assert count_syllables_word("11") == 3  # e-lev-en
    assert count_syllables_word("100") == 3  # one hun-dred


def test_punctuation_stripped():
    assert count_syllables_word("hello!") == 2
    assert count_syllables_word("world,") == 1
    assert count_syllables_word("(test)") == 1


def test_empty_string():
    assert count_syllables_word("") == 0
    assert count_syllables_word("!!!") == 0


def test_simple_sentences():
    assert count_syllables("hello world") == 3
    assert count_syllables("the cat sat") == 3


def test_haiku_lines():
    assert count_syllables("An old silent pond") == 5
    assert count_syllables("A frog jumps into the pond") == 7
    assert count_syllables("Splash silence again") == 5


def test_with_numbers():
    assert count_syllables("First shot day in 3 years") == 6
    assert count_syllables("I have 2 cats") == 4
    assert count_syllables("100 days of code") == 6  # one-hun-dred days of code
