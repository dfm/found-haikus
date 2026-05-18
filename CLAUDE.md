# Haiku Feed Generator

Bluesky custom feed that assembles haikus from posts by finding triplets with 5-7-5 syllable patterns.

## Architecture

- **Firehose consumer** (`haiku/firehose.py`): Connects to Bluesky relay via `atproto`, filters English text posts without replies/embeds, classifies 5/7-syllable lines via the `syllables` library (`is_haiku_line`, conservative — abstains rather than guesses; `HAIKU_FUZZINESS` tunes precision/coverage)
- **Haiku matcher** (`haiku/matcher.py`): Buffers 5 and 7 syllable posts, assembles haikus when a valid 5-7-5 triplet is found
- **Database** (`haiku/db.py`): SQLite storage for haiku URIs, auto-cleans to keep most recent 10,000
- **Feed server** (`haiku/server.py`): Flask app implementing `app.bsky.feed.getFeedSkeleton` with pagination

## Deployment

Deployed on Fly.io at https://found-haikus.fly.dev/

- Single VM runs both worker and server via `scripts/start.sh`
- Worker imports `syllables` (pinned to a git commit; bundles a ~450KB lexicon + tiny JAX model, pulls in jax/jaxlib/scipy), server stays lightweight
- Volume mounted at `/data` for SQLite persistence

```
fly deploy
fly logs --app found-haikus
```

## Local Development

```
uv sync
uv run haiku --db haiku.db    # run firehose worker
uv run haiku-serve --db haiku.db  # run feed server
uv run pytest                 # run tests
```

## Code Style

- Minimal comments - code should be self-explanatory
- No docstrings unless API documentation is needed
- Tests use top-level functions, not classes
- Formatting and linting via ruff
