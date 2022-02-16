import sqlite3
from typing import Iterator
from contextlib import contextmanager

DB_FILE = "data/data.db"


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_FILE)
    yield conn
    conn.commit()