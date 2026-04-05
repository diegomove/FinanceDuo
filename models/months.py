"""Month model queries."""

import sqlite3
from datetime import date

from flask import session

from translations import DEFAULT_LANG, MONTH_NAMES


def get_all(db: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return all months ordered by year desc, month desc."""
    return db.execute(
        "SELECT id, year, month, is_closed FROM months ORDER BY year DESC, month DESC"
    ).fetchall()


def get_by_id(db: sqlite3.Connection, month_id: int) -> sqlite3.Row | None:
    """Return a month by ID."""
    return db.execute(
        "SELECT id, year, month, is_closed FROM months WHERE id = ?",
        (month_id,),
    ).fetchone()


def create(db: sqlite3.Connection, year: int, month: int) -> int | None:
    """Create a new month. Returns the new ID or None if it already exists."""
    try:
        cursor = db.execute(
            "INSERT INTO months (year, month) VALUES (?, ?)", (year, month)
        )
        db.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def toggle_closed(db: sqlite3.Connection, month_id: int) -> None:
    """Toggle the is_closed flag on a month."""
    db.execute(
        "UPDATE months SET is_closed = CASE WHEN is_closed = 0 THEN 1 ELSE 0 END WHERE id = ?",
        (month_id,),
    )
    db.commit()


def copy_fixed_expenses(
    db: sqlite3.Connection, source_id: int, target_id: int
) -> int:
    """Copy fixed-category expected expenses from source month to target.

    Returns the number of rows copied.
    """
    cursor = db.execute(
        """
        INSERT OR IGNORE INTO expected_expenses (month_id, category_id, amount, notes, paid_by)
        SELECT ?, ee.category_id, ee.amount, ee.notes, ee.paid_by
        FROM expected_expenses ee
        JOIN categories c ON c.id = ee.category_id
        WHERE ee.month_id = ? AND c.type = 'fixed'
        """,
        (target_id, source_id),
    )
    db.commit()
    return cursor.rowcount


def get_previous(db: sqlite3.Connection, month_id: int) -> sqlite3.Row | None:
    """Return the most recent month before the given one."""
    current = get_by_id(db, month_id)
    if current is None:
        return None
    return db.execute(
        """
        SELECT id, year, month, is_closed FROM months
        WHERE (year < ? OR (year = ? AND month < ?))
        ORDER BY year DESC, month DESC
        LIMIT 1
        """,
        (current["year"], current["year"], current["month"]),
    ).fetchone()


def get_display_name(month_row: sqlite3.Row, lang: str | None = None) -> str:
    """Return a display name like 'April 2026'."""
    if lang is None:
        lang = session.get("lang", DEFAULT_LANG)
    names = MONTH_NAMES.get(lang, MONTH_NAMES[DEFAULT_LANG])
    return f"{names[month_row['month']]} {month_row['year']}"


def get_current_year_month() -> tuple[int, int]:
    """Return the current (year, month) tuple."""
    today = date.today()
    return today.year, today.month


def get_month_summary(db: sqlite3.Connection, month_id: int) -> dict:
    """Return quick stats for a month: income, budgeted, actual spent."""
    row = db.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM income WHERE month_id = ?",
        (month_id,),
    ).fetchone()
    income = row["total"]

    row = db.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM expected_expenses WHERE month_id = ?",
        (month_id,),
    ).fetchone()
    budgeted = row["total"]

    row = db.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM actual_expenses WHERE month_id = ?",
        (month_id,),
    ).fetchone()
    actual = row["total"]

    return {
        "income": income,
        "budgeted": budgeted,
        "actual": actual,
        "budget_pct": (actual / budgeted * 100) if budgeted > 0 else 0,
    }
