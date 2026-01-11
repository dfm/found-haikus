# Haiku Feed Generator

BlueSky custom feed that assembles haikus from posts by finding triplets with 5-7-5 syllable patterns.

## Architecture

- **Firehose consumer**: Connects to BlueSky relay via `atproto` library, filters for `app.bsky.feed.post` creates
- **CAR parsing**: Records are extracted from CAR (Content Addressable aRchive) blocks using the operation's CID
- **Feed generator**: (TODO) HTTP server implementing `app.bsky.feed.getFeedSkeleton`

## AT Protocol Notes

- Firehose messages contain: commits (with ops), identity updates, handle changes, etc.
- Each commit has `ops` (operations) and `blocks` (CAR-encoded record data)
- `RepoOp` contains: `action` (create/update/delete), `path` (collection/rkey), `cid` (reference to record in blocks)
- Post path format: `app.bsky.feed.post/{rkey}`
- Author DID is in `commit.repo`

## Running

```
uv sync
uv run haiku
```

## Code Style

- Minimal comments - code should be self-explanatory
- No docstrings unless API documentation is needed
- Tests use top-level functions, not classes
- Formatting and linting via ruff
