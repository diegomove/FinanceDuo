"""People model queries."""

import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash


def get_all(db: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return all people."""
    return db.execute("SELECT id, name FROM people ORDER BY id").fetchall()


def get_by_id(db: sqlite3.Connection, person_id: int) -> sqlite3.Row | None:
    """Return a person by ID."""
    return db.execute(
        "SELECT id, name FROM people WHERE id = ?", (person_id,)
    ).fetchone()


def get_by_name(db: sqlite3.Connection, name: str) -> sqlite3.Row | None:
    """Return a person by name (case-insensitive)."""
    return db.execute(
        "SELECT id, name, password_hash FROM people WHERE LOWER(name) = LOWER(?)",
        (name,),
    ).fetchone()


def verify_password(db: sqlite3.Connection, person_id: int, password: str) -> bool:
    """Check if the password matches for a person."""
    row = db.execute(
        "SELECT password_hash FROM people WHERE id = ?", (person_id,)
    ).fetchone()
    if row is None or row["password_hash"] is None:
        return False
    return check_password_hash(row["password_hash"], password)


def set_password(db: sqlite3.Connection, person_id: int, password: str) -> None:
    """Set a new password for a person."""
    pw_hash = generate_password_hash(password)
    db.execute(
        "UPDATE people SET password_hash = ? WHERE id = ?", (pw_hash, person_id)
    )
    db.commit()
