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

## Development

```bash
uv run pytest           # run tests
uv run ruff check .     # lint
uv run ruff format .    # format
```

## License

MIT
