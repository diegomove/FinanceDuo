"""Database connection helpers."""

import sqlite3
from pathlib import Path

from flask import Flask, g


def get_db() -> sqlite3.Connection:
    """Get or create a database connection for the current request."""
    if "db" not in g:
        from config import DATABASE

        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e: BaseException | None = None) -> None:
    """Close the database connection at end of request."""
    db: sqlite3.Connection | None = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app: Flask) -> None:
    """Register database teardown with the Flask app."""
    app.teardown_appcontext(close_db)
