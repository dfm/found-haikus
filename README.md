# Haikus Found on Bluesky

Millions of people are posting to Bluesky every day. Some of those posts have exactly 5 syllables. Others have exactly 7. What happens when you string them together?

```
========================================
Big crows will take us.
Way too early to score, Bills
Yeah, it's happening.
========================================
```

Poetry, that's what.

## Try it yourself

```bash
git clone https://github.com/dfm/haiku.git
cd haiku
uv sync
uv run haiku
```

Watch the haikus roll in. Pass `--db haiku.db` to save them to a SQLite database.

## Deploy to Fly.io

```bash
# Create the app and volume
fly launch --no-deploy
fly volumes create haiku_data --region ewr --size 1

# Set your secrets
fly secrets set FEEDGEN_HOSTNAME=your-app.fly.dev
fly secrets set FEEDGEN_PUBLISHER_DID=did:plc:your-did

# Deploy
fly deploy

# Publish the feed to your Bluesky account (once)
BSKY_HANDLE=you.bsky.social \
BSKY_PASSWORD=your-app-password \
FEEDGEN_HOSTNAME=your-app.fly.dev \
python scripts/publish_feed.py
```

## Development

```bash
uv run pytest           # run tests
uv run ruff check .     # lint
uv run ruff format .    # format
```

## License

MIT
