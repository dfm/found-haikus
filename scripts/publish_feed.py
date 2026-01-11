#!/usr/bin/env python3
"""Publish the haiku feed generator to Bluesky.

Required environment variables:
- BSKY_HANDLE: Your Bluesky handle (e.g., alice.bsky.social)
- BSKY_PASSWORD: Your Bluesky app password
- FEEDGEN_HOSTNAME: The hostname where your feed is hosted (e.g., haiku.example.com)
"""

import os
import sys

from atproto import Client, models


def main():
    handle = os.environ.get("BSKY_HANDLE")
    password = os.environ.get("BSKY_PASSWORD")
    hostname = os.environ.get("FEEDGEN_HOSTNAME")

    if not all([handle, password, hostname]):
        print("Missing required environment variables:")
        print("  BSKY_HANDLE - Your Bluesky handle")
        print("  BSKY_PASSWORD - Your Bluesky app password")
        print("  FEEDGEN_HOSTNAME - Your feed server hostname")
        sys.exit(1)

    client = Client()
    client.login(handle, password)

    feed_did = f"did:web:{hostname}"

    record = models.AppBskyFeedGenerator.Record(
        did=feed_did,
        display_name="Haiku",
        description="Haikus found on Bluesky. Three posts, 5-7-5 syllables, assembled into poetry.",
        created_at=client.get_current_time_iso(),
    )

    uri = client.app.bsky.feed.generator.create(client.me.did, record, rkey="haiku")

    print("Feed published!")
    print(f"Feed URI: {uri.uri}")
    print(f"Feed DID: {feed_did}")
    print("\nYour feed should now be available at:")
    print(f"  https://bsky.app/profile/{handle}/feed/haiku")


if __name__ == "__main__":
    main()
