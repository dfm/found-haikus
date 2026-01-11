import re

from atproto import CAR, parse_subscribe_repos_message

from haiku.matcher import HaikuMatcher
from haiku.syllables import count_syllables

SKIP_FACET_TYPES = {
    "app.bsky.richtext.facet#tag",
    "app.bsky.richtext.facet#link",
}

MAX_CHARS = 50
MAX_WORDS = 12
HAIKU_SYLLABLES = {5, 7}

TRAILING_NON_ALPHA = re.compile(r"[^\w\s]*\s*$")
RANDOM_STRING = re.compile(r"(?=.*[0-9])(?=.*[A-Za-z])[A-Za-z0-9]{12,}")


def is_letter_or_ascii(char: str) -> bool:
    return char.isascii() or char.isalpha()


def is_english_text_only(record: dict) -> bool:
    langs = record.get("langs", [])
    if not langs or "en" not in langs:
        return False

    if record.get("embed"):
        return False

    if record.get("labels"):
        return False

    for facet in record.get("facets", []):
        for feature in facet.get("features", []):
            if feature.get("$type") in SKIP_FACET_TYPES:
                return False

    return True


def has_emoji_in_middle(text: str) -> bool:
    without_trailing = TRAILING_NON_ALPHA.sub("", text)
    return not all(is_letter_or_ascii(c) for c in without_trailing)


def could_be_haiku_line(text: str) -> bool:
    if len(text) > MAX_CHARS:
        return False
    words = text.split()
    return len(words) <= MAX_WORDS


def is_quality_text(text: str) -> bool:
    if text.lower().startswith("macro:"):
        return False

    letters = [c for c in text if c.isalpha()]
    if len(letters) >= 4:
        upper_count = sum(1 for c in letters if c.isupper())
        if upper_count == len(letters):
            return False

    return not RANDOM_STRING.search(text)


def create_message_handler(matcher: HaikuMatcher, on_haiku):
    def on_message_handler(message) -> None:
        commit = parse_subscribe_repos_message(message)

        if not hasattr(commit, "ops") or not commit.ops:
            return
        if not commit.blocks:
            return

        car = CAR.from_bytes(commit.blocks)

        for op in commit.ops:
            if op.action != "create":
                continue
            if not op.path.startswith("app.bsky.feed.post/"):
                continue
            if not op.cid:
                continue

            record = car.blocks.get(op.cid)
            if not record or not isinstance(record, dict):
                continue
            if not is_english_text_only(record):
                continue

            text = record.get("text", "").strip()
            if not text:
                continue
            if has_emoji_in_middle(text):
                continue
            if not could_be_haiku_line(text):
                continue
            if not is_quality_text(text):
                continue

            syllables = count_syllables(text)
            if syllables not in HAIKU_SYLLABLES:
                continue

            uri = f"at://{commit.repo}/{op.path}"
            haiku = matcher.add_post(uri, text, syllables)
            if haiku:
                on_haiku(haiku)

    return on_message_handler
