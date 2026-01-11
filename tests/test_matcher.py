from haiku.matcher import Haiku, HaikuMatcher, Post


def test_no_match_with_insufficient_posts():
    matcher = HaikuMatcher()
    assert matcher.add_post("uri1", "five syllables here", 5) is None
    assert matcher.add_post("uri2", "seven syllables in this line", 7) is None


def test_match_with_two_fives_and_one_seven():
    matcher = HaikuMatcher()
    matcher.add_post("uri1", "first line five", 5)
    matcher.add_post("uri2", "second line seven here", 7)
    haiku = matcher.add_post("uri3", "third line five", 5)

    assert haiku is not None
    assert haiku.line1.text == "first line five"
    assert haiku.line2.text == "second line seven here"
    assert haiku.line3.text == "third line five"


def test_match_uses_fifo_order():
    matcher = HaikuMatcher()
    matcher.add_post("uri1", "first five", 5)
    matcher.add_post("uri2", "second five", 5)
    matcher.add_post("uri3", "third five", 5)

    # Haiku forms immediately when we have 2+ fives and 1 seven
    haiku = matcher.add_post("uri4", "first seven", 7)

    assert haiku is not None
    assert haiku.line1.text == "first five"
    assert haiku.line2.text == "first seven"
    assert haiku.line3.text == "second five"


def test_multiple_haikus():
    matcher = HaikuMatcher()

    matcher.add_post("uri1", "five one", 5)
    matcher.add_post("uri2", "seven one", 7)
    haiku1 = matcher.add_post("uri3", "five two", 5)

    assert haiku1 is not None
    assert haiku1.line1.text == "five one"

    matcher.add_post("uri4", "five three", 5)
    matcher.add_post("uri5", "seven two", 7)
    haiku2 = matcher.add_post("uri6", "five four", 5)

    assert haiku2 is not None
    assert haiku2.line1.text == "five three"


def test_buffer_limit():
    # buffer_size=1 means fives buffer holds 2, sevens buffer holds 1
    matcher = HaikuMatcher(buffer_size=1)

    matcher.add_post("uri1", "old five", 5)
    matcher.add_post("uri2", "newer five", 5)
    matcher.add_post("uri3", "newest five", 5)  # pushes out "old five"

    # Haiku forms when we add the seven
    haiku = matcher.add_post("uri4", "a seven", 7)

    assert haiku is not None
    assert haiku.line1.text == "newer five"  # "old five" was evicted
    assert haiku.line2.text == "a seven"
    assert haiku.line3.text == "newest five"


def test_post_dataclass():
    post = Post(uri="at://did:plc:123/app.bsky.feed.post/abc", text="hello", syllables=5)
    assert post.uri == "at://did:plc:123/app.bsky.feed.post/abc"
    assert post.text == "hello"
    assert post.syllables == 5


def test_haiku_str():
    haiku = Haiku(
        line1=Post(uri="uri1", text="An old silent pond", syllables=5),
        line2=Post(uri="uri2", text="A frog jumps into the pond", syllables=7),
        line3=Post(uri="uri3", text="Splash silence again", syllables=5),
    )
    assert str(haiku) == "An old silent pond\nA frog jumps into the pond\nSplash silence again"
