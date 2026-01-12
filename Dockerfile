FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY haiku ./haiku
COPY scripts ./scripts

# Install dependencies
RUN uv sync --frozen --no-dev

# Create data directory for SQLite
RUN mkdir -p /data

ENV PATH="/app/.venv/bin:$PATH"
ENV FEEDGEN_DB_PATH="/data/haiku.db"

EXPOSE 8080
