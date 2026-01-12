#!/bin/bash
set -e

# Initialize the database
python -c "from haiku.db import init_db; from pathlib import Path; init_db(Path('/data/haiku.db'))"

# Start the worker in the background
python -m haiku.main --db /data/haiku.db &

# Start the web server
exec gunicorn haiku.server:app --bind 0.0.0.0:8080
