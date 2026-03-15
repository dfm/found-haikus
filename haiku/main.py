import argparse
import logging
import sys
import time
from pathlib import Path

from atproto import FirehoseSubscribeReposClient

from haiku.db import init_db, save_haiku
from haiku.firehose import create_message_handler
from haiku.matcher import HaikuMatcher

RESTART_DELAY = 5
MAX_RESTART_DELAY = 300

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


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

    delay = RESTART_DELAY
    while True:
        matcher = HaikuMatcher()
        handler = create_message_handler(matcher, on_haiku)
        client = FirehoseSubscribeReposClient()
        try:
            logger.info("Connecting to firehose...")
            client.start(handler)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            sys.exit(0)
        except Exception:
            logger.exception("Firehose connection error")
        logger.info("Restarting in %ds...", delay)
        time.sleep(delay)
        delay = min(delay * 2, MAX_RESTART_DELAY)


if __name__ == "__main__":
    main()
