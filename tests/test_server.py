import os
import tempfile
from pathlib import Path

import pytest

from haiku.db import init_db, save_haiku
from haiku.matcher import Haiku, Post


@pytest.fixture
def app():
    os.environ["FEEDGEN_HOSTNAME"] = "haiku.example.com"
    os.environ["FEEDGEN_PUBLISHER_DID"] = "did:plc:testuser"

    from haiku.server import app

    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_did_document(client):
    response = client.get("/.well-known/did.json")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == "did:web:haiku.example.com"
    assert data["service"][0]["type"] == "BskyFeedGenerator"
    assert data["service"][0]["serviceEndpoint"] == "https://haiku.example.com"


def test_describe_feed_generator(client):
    response = client.get("/xrpc/app.bsky.feed.describeFeedGenerator")
    assert response.status_code == 200
    data = response.get_json()
    assert data["did"] == "did:web:haiku.example.com"
    assert len(data["feeds"]) == 1
    assert data["feeds"][0]["uri"] == "at://did:plc:testuser/app.bsky.feed.generator/haiku"


def test_get_feed_skeleton_unknown_feed(client):
    response = client.get("/xrpc/app.bsky.feed.getFeedSkeleton?feed=at://unknown/feed")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "UnknownFeed"


def test_get_feed_skeleton_empty(client):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    try:
        init_db(db_path)
        os.environ["FEEDGEN_DB_PATH"] = str(db_path)

        feed_uri = "at://did:plc:testuser/app.bsky.feed.generator/haiku"
        response = client.get(f"/xrpc/app.bsky.feed.getFeedSkeleton?feed={feed_uri}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["feed"] == []
        assert "cursor" not in data
    finally:
        db_path.unlink()


def test_get_feed_skeleton_with_haikus(client):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    try:
        init_db(db_path)
        os.environ["FEEDGEN_DB_PATH"] = str(db_path)

        haiku = Haiku(
            line1=Post(uri="at://did:plc:a/post/1", text="line one", syllables=5),
            line2=Post(uri="at://did:plc:a/post/2", text="line two", syllables=7),
            line3=Post(uri="at://did:plc:a/post/3", text="line three", syllables=5),
        )
        save_haiku(haiku, db_path)

        feed_uri = "at://did:plc:testuser/app.bsky.feed.generator/haiku"
        response = client.get(f"/xrpc/app.bsky.feed.getFeedSkeleton?feed={feed_uri}")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["feed"]) == 3
        assert data["feed"][0]["post"] == "at://did:plc:a/post/1"
        assert data["feed"][1]["post"] == "at://did:plc:a/post/2"
        assert data["feed"][2]["post"] == "at://did:plc:a/post/3"
    finally:
        db_path.unlink()


def test_get_feed_skeleton_pagination(client):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    try:
        init_db(db_path)
        os.environ["FEEDGEN_DB_PATH"] = str(db_path)

        # Create 3 haikus
        for i in range(3):
            haiku = Haiku(
                line1=Post(uri=f"at://did:plc:a/post/{i}a", text="line", syllables=5),
                line2=Post(uri=f"at://did:plc:a/post/{i}b", text="line", syllables=7),
                line3=Post(uri=f"at://did:plc:a/post/{i}c", text="line", syllables=5),
            )
            save_haiku(haiku, db_path)

        feed_uri = "at://did:plc:testuser/app.bsky.feed.generator/haiku"

        # Get first page (limit=3 means 1 haiku)
        response = client.get(f"/xrpc/app.bsky.feed.getFeedSkeleton?feed={feed_uri}&limit=3")
        data = response.get_json()
        assert len(data["feed"]) == 3
        assert "cursor" in data

        # Get second page using cursor
        cursor = data["cursor"]
        response = client.get(
            f"/xrpc/app.bsky.feed.getFeedSkeleton?feed={feed_uri}&limit=3&cursor={cursor}"
        )
        data = response.get_json()
        assert len(data["feed"]) == 3
        assert "cursor" in data

        # Get third page
        cursor = data["cursor"]
        response = client.get(
            f"/xrpc/app.bsky.feed.getFeedSkeleton?feed={feed_uri}&limit=3&cursor={cursor}"
        )
        data = response.get_json()
        assert len(data["feed"]) == 3
        assert "cursor" not in data  # No more pages
    finally:
        db_path.unlink()
