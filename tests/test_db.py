from haiku.db import get_recent_haikus, init_db, save_haiku
from haiku.matcher import Haiku, Post


def test_init_db(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    assert db_path.exists()


def test_save_and_retrieve_haiku(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)

    haiku = Haiku(
        line1=Post(uri="at://did:1/post/1", text="An old silent pond", syllables=5),
        line2=Post(uri="at://did:2/post/2", text="A frog jumps into the pond", syllables=7),
        line3=Post(uri="at://did:3/post/3", text="Splash silence again", syllables=5),
    )

    haiku_id = save_haiku(haiku, db_path)
    assert haiku_id == 1

    haikus = get_recent_haikus(limit=10, db_path=db_path)
    assert len(haikus) == 1
    assert haikus[0]["line1_text"] == "An old silent pond"
    assert haikus[0]["line2_text"] == "A frog jumps into the pond"
    assert haikus[0]["line3_text"] == "Splash silence again"


def test_recent_haikus_ordering(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)

    for i in range(5):
        haiku = Haiku(
            line1=Post(uri=f"uri{i}a", text=f"Line one {i}", syllables=5),
            line2=Post(uri=f"uri{i}b", text=f"Line two {i}", syllables=7),
            line3=Post(uri=f"uri{i}c", text=f"Line three {i}", syllables=5),
        )
        save_haiku(haiku, db_path)

    haikus = get_recent_haikus(limit=3, db_path=db_path)
    assert len(haikus) == 3
    assert haikus[0]["line1_text"] == "Line one 4"  # most recent first
    assert haikus[1]["line1_text"] == "Line one 3"
    assert haikus[2]["line1_text"] == "Line one 2"
