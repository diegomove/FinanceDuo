"""Initialize the database: create tables and seed data."""

import os
import secrets
import sqlite3
from pathlib import Path

from werkzeug.security import generate_password_hash

from config import DATABASE, PERSON1_NAME, PERSON2_NAME

SCHEMA_PATH: Path = Path(__file__).resolve().parent / "schema.sql"

SEED_PEOPLE: list[str] = [PERSON1_NAME, PERSON2_NAME]

SEED_CATEGORIES: list[tuple[str, str]] = [
    ("Rent", "fixed"),
    ("WiFi", "fixed"),
    ("Insurance", "fixed"),
    ("Subscriptions", "fixed"),
    ("Phone", "fixed"),
    ("Groceries", "variable"),
    ("Energy", "variable"),
    ("Water", "variable"),
    ("Transport", "variable"),
    ("Dining Out", "extra"),
    ("Entertainment", "extra"),
    ("Shopping", "extra"),
    ("Health", "extra"),
    ("Other", "extra"),
]

DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD") or secrets.token_urlsafe(10)


def init_db() -> None:
    """Create tables and insert seed data."""
    db = sqlite3.connect(DATABASE)

    schema_sql = SCHEMA_PATH.read_text()
    db.executescript(schema_sql)

    for name in SEED_PEOPLE:
        db.execute(
            "INSERT OR IGNORE INTO people (name, password_hash) VALUES (?, ?)",
            (name, generate_password_hash(DEFAULT_PASSWORD)),
        )

    for name, cat_type in SEED_CATEGORIES:
        db.execute(
            "INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)",
            (name, cat_type),
        )

    db.commit()
    db.close()
    print(f"Database initialized at {DATABASE}")
    print(f"People: {', '.join(SEED_PEOPLE)}")
    print(f"Initial password for all users: {DEFAULT_PASSWORD}")
    print("IMPORTANT: Change passwords after first login via Settings.")


if __name__ == "__main__":
    init_db()
