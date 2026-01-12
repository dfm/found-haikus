import argparse
from pathlib import Path

from atproto import FirehoseSubscribeReposClient
from atproto.exceptions import FirehoseError

from haiku.db import init_db, save_haiku
from haiku.firehose import create_message_handler
from haiku.matcher import HaikuMatcher


def main():
    parser = argparse.ArgumentParser(description="Find haikus on Bluesky")
    parser.add_argument(
        "--db",
        type=Path,
        metavar="FILE",
        help="Save haikus to this SQLite database",
    )
    args = parser.parse_args()

    if args.db:
        init_db(args.db)

        def on_haiku(haiku):
            haiku_id = save_haiku(haiku, args.db)
            if haiku_id % 1000 == 0:
                print(f"\n{'=' * 40}\n{haiku}\n{'=' * 40}\n")

    else:

        def on_haiku(haiku):
            print(f"\n{'=' * 40}\n{haiku}\n{'=' * 40}\n")

    matcher = HaikuMatcher()
    handler = create_message_handler(matcher, on_haiku)
    client = FirehoseSubscribeReposClient()
    try:
        client.start(handler)
    except FirehoseError as e:
        print(f"Firehose error: {e}")
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    main()
