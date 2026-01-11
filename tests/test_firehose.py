from haiku.firehose import has_emoji_in_middle, is_quality_text


def test_plain_ascii():
    assert not has_emoji_in_middle("Hello world")
    assert not has_emoji_in_middle("The cat sat on the mat")


def test_trailing_emoji_allowed():
    assert not has_emoji_in_middle("Hello 😀")
    assert not has_emoji_in_middle("Nice day! 🌞")
    assert not has_emoji_in_middle("Test 🎉🎉🎉")
    assert not has_emoji_in_middle("Good morning ☀️🌈")


def test_trailing_emoji_with_whitespace():
    assert not has_emoji_in_middle("Hello 😀  ")
    assert not has_emoji_in_middle("Test 🎉 ")


def test_emoji_in_middle_rejected():
    assert has_emoji_in_middle("Hello 😀 world")
    assert has_emoji_in_middle("I 💕 coding")
    assert has_emoji_in_middle("🎉 Party time")


def test_accented_letters_allowed():
    assert not has_emoji_in_middle("Café is great")
    assert not has_emoji_in_middle("naïve approach")
    assert not has_emoji_in_middle("résumé")


def test_empty_and_whitespace():
    assert not has_emoji_in_middle("")
    assert not has_emoji_in_middle("   ")


def test_quality_normal_text():
    assert is_quality_text("Hello world")
    assert is_quality_text("An old silent pond")
    assert is_quality_text("I love this!")


def test_quality_rejects_macro():
    assert not is_quality_text("macro: EiuLi8p9cfIkbQLqQ2Rn")
    assert not is_quality_text("Macro: something here")
    assert not is_quality_text("MACRO: test")


def test_quality_rejects_all_caps():
    assert not is_quality_text("NOW PLEASE PLAY DEFENSE")
    assert not is_quality_text("THIS IS ALL CAPS")
    assert is_quality_text("OK")  # too short to reject
    assert is_quality_text("Hello WORLD")  # mixed case is fine


def test_quality_rejects_random_strings():
    assert not is_quality_text("EiuLi8p9cfIkbQLqQ2Rn")
    assert not is_quality_text("Check this: AyoqM3jawcKVr4UponOg")
    assert is_quality_text("Hello world")  # normal text
    assert is_quality_text("Unbelievable")  # long words are fine
    assert is_quality_text("Congratulations")  # all letters, no digits


def test_quality_allows_repeated_chars():
    assert is_quality_text("Noooooo")
    assert is_quality_text("Yessssss")
    assert is_quality_text("Hahahaha")
