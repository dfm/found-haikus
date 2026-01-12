import sqlite3
from contextlib import contextmanager
from pathlib import Path

from haiku.matcher import Haiku

DEFAULT_DB_PATH = Path("haiku.db")
MAX_HAIKUS = 10000


def init_db(db_path: Path = DEFAULT_DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS haikus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                line1_uri TEXT NOT NULL,
                line2_uri TEXT NOT NULL,
                line3_uri TEXT NOT NULL
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
            INSERT INTO haikus (line1_uri, line2_uri, line3_uri)
            VALUES (?, ?, ?)
            """,
            (haiku.line1.uri, haiku.line2.uri, haiku.line3.uri),
        )
        haiku_id = cursor.lastrowid

        # Clean up old entries
        conn.execute(
            """
            DELETE FROM haikus
            WHERE id <= (SELECT id FROM haikus ORDER BY id DESC LIMIT 1 OFFSET ?)
            """,
            (MAX_HAIKUS,),
        )

        return haiku_id


def get_recent_haikus(
    limit: int = 50, db_path: Path = DEFAULT_DB_PATH, after_id: int | None = None
) -> list[dict]:
    with get_connection(db_path) as conn:
        if after_id is not None:
            cursor = conn.execute(
                """
                SELECT id, created_at, line1_uri, line2_uri, line3_uri
                FROM haikus
                WHERE id < ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (after_id, limit),
            )
        else:
            cursor = conn.execute(
                """
                SELECT id, created_at, line1_uri, line2_uri, line3_uri
                FROM haikus
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            )
        return [dict(row) for row in cursor.fetchall()]
