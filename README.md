# Haiku Feed Generator

A BlueSky custom feed that assembles haikus from the firehose by finding triplets of posts with 5-7-5 syllable patterns.

## How it works

1. Connects to the BlueSky firehose via the AT Protocol
2. Filters for English text-only posts (no images, links, hashtags)
3. Counts syllables using the CMU Pronouncing Dictionary
4. Buffers posts with exactly 5 or 7 syllables
5. Assembles haikus when matching 5-7-5 triplets are found

Example output:

```
========================================
Big crows will take us.
Way too early to score, Bills
Yeah, it's happening.
========================================
```

## Installation

Requires Python 3.13+.

```bash
git clone https://github.com/dfm/haiku.git
cd haiku
uv sync
```

## Usage

### Watch haikus form (without saving)

```bash
uv run haiku --no-save
```

### Save haikus to database

```bash
uv run haiku
```

Haikus are stored in `haiku.db` (SQLite).

## Development

### Run tests

```bash
uv run pytest
```

### Lint and format

```bash
uv run ruff check .
uv run ruff format .
```

## Filtering

Posts are filtered to improve haiku quality:

- **English only** - posts must have `en` in their language tags
- **Text only** - no images, videos, or embeds
- **No links or hashtags** - pure text content
- **No NSFW** - posts with content labels are skipped
- **No emoji in middle** - trailing emoji are allowed
- **No all-caps** - posts with 4+ letters must have mixed case
- **No random strings** - filters out tokens/hashes (12+ alphanumeric with mixed letters and digits)
- **No macros** - filters out FFXIV game macros

## License

MIT
