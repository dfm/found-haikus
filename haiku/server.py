import contextlib
import os
from pathlib import Path

from flask import Flask, jsonify, request

from haiku.db import get_recent_haikus

HOSTNAME = os.environ.get("FEEDGEN_HOSTNAME", "localhost")
PUBLISHER_DID = os.environ.get("FEEDGEN_PUBLISHER_DID", "")
FEED_URI = f"at://{PUBLISHER_DID}/app.bsky.feed.generator/haiku"

app = Flask(__name__)


@app.route("/.well-known/did.json")
def did_document():
    service_did = f"did:web:{HOSTNAME}"
    return jsonify(
        {
            "@context": ["https://www.w3.org/ns/did/v1"],
            "id": service_did,
            "service": [
                {
                    "id": "#bsky_fg",
                    "type": "BskyFeedGenerator",
                    "serviceEndpoint": f"https://{HOSTNAME}",
                }
            ],
        }
    )


@app.route("/xrpc/app.bsky.feed.describeFeedGenerator")
def describe_feed_generator():
    service_did = f"did:web:{HOSTNAME}"
    return jsonify(
        {
            "did": service_did,
            "feeds": [{"uri": FEED_URI}],
        }
    )


@app.route("/xrpc/app.bsky.feed.getFeedSkeleton")
def get_feed_skeleton():
    feed = request.args.get("feed", "")
    cursor = request.args.get("cursor", "")
    limit = min(int(request.args.get("limit", 50)), 100)

    if feed != FEED_URI:
        return jsonify({"error": "UnknownFeed", "message": "Unknown feed"}), 400

    db_path = Path(os.environ.get("FEEDGEN_DB_PATH", "haiku.db"))

    # Parse cursor (format: "id:123" or empty for start)
    after_id = None
    if cursor and cursor.startswith("id:"):
        with contextlib.suppress(ValueError):
            after_id = int(cursor[3:])

    # We need limit/3 haikus since each haiku has 3 posts
    haiku_limit = max(limit // 3, 1)
    haikus = get_recent_haikus(limit=haiku_limit + 1, db_path=db_path, after_id=after_id)

    # Build feed from haiku post URIs
    feed_items = []
    for haiku in haikus[:haiku_limit]:
        feed_items.append({"post": haiku["line1_uri"]})
        feed_items.append({"post": haiku["line2_uri"]})
        feed_items.append({"post": haiku["line3_uri"]})

    # Set cursor if there are more results
    next_cursor = None
    if len(haikus) > haiku_limit:
        last_haiku = haikus[haiku_limit - 1]
        next_cursor = f"id:{last_haiku['id']}"

    response = {"feed": feed_items}
    if next_cursor:
        response["cursor"] = next_cursor

    return jsonify(response)


def serve():
    import argparse

    parser = argparse.ArgumentParser(description="Serve the haiku feed")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=3000, help="Port to bind to")
    parser.add_argument("--db", type=Path, default=Path("haiku.db"), help="Database path")
    args = parser.parse_args()

    os.environ["FEEDGEN_DB_PATH"] = str(args.db)

    print(f"Starting feed server on {args.host}:{args.port}")
    print(f"Database: {args.db}")
    app.run(host=args.host, port=args.port, debug=True)
