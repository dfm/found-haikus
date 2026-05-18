FROM python:3.13-slim

WORKDIR /app

# git: uv needs it to resolve the syllables git+https dependency
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml uv.lock README.md ./
COPY haiku ./haiku
COPY scripts ./scripts

# Install dependencies
RUN uv sync --frozen --no-dev

# Create data directory for SQLite
RUN mkdir -p /data

# Make start script executable
RUN chmod +x scripts/start.sh

ENV PATH="/app/.venv/bin:$PATH"
ENV FEEDGEN_DB_PATH="/data/haiku.db"

EXPOSE 8080

CMD ["scripts/start.sh"]
