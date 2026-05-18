from syllables import is_haiku_line

from haiku.firehose import HAIKU_FUZZINESS


def test_classic_haiku_lines():
    assert is_haiku_line("An old silent pond") == 5
    assert is_haiku_line("A frog jumps into the pond") == 7
    assert is_haiku_line("Splash silence again") == 5


def test_returns_5_7_or_none():
    for text in ["An old silent pond", "A frog jumps into the pond", "zqxwvb??"]:
        result = is_haiku_line(text)
        assert result in (5, 7, None)


def test_abstains_on_junk():
    assert is_haiku_line("zqxwvb??") is None
    assert is_haiku_line("hhFDWkdAxDjkbJfXdOwv") is None


def test_fuzziness_kwarg_accepted():
    assert is_haiku_line("An old silent pond", fuzziness=HAIKU_FUZZINESS) == 5
