import sqlite3
from contextlib import contextmanager
from pathlib import Path

from haiku.matcher import Haiku

DEFAULT_DB_PATH = Path("haiku.db")


def init_db(db_path: Path = DEFAULT_DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS haikus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                line1_uri TEXT NOT NULL,
                line1_text TEXT NOT NULL,
                line2_uri TEXT NOT NULL,
                line2_text TEXT NOT NULL,
                line3_uri TEXT NOT NULL,
                line3_text TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_haikus_created_at ON haikus (created_at DESC)
        """)


@contextmanager
def get_connection(db_path: Path = DEFAULT_DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def save_haiku(haiku: Haiku, db_path: Path = DEFAULT_DB_PATH) -> int:
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO haikus (line1_uri, line1_text, line2_uri, line2_text, line3_uri, line3_text)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                haiku.line1.uri,
                haiku.line1.text,
                haiku.line2.uri,
                haiku.line2.text,
                haiku.line3.uri,
                haiku.line3.text,
            ),
        )
        return cursor.lastrowid


def get_recent_haikus(limit: int = 50, db_path: Path = DEFAULT_DB_PATH) -> list[dict]:
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT id, created_at,
                   line1_uri, line1_text,
                   line2_uri, line2_text,
                   line3_uri, line3_text
            FROM haikus
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]
