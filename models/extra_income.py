"""Extra income model: Bizums, refunds, and other non-salary income."""

import sqlite3


def get_all_for_month(
    db: sqlite3.Connection, month_id: int, person_filter: int | None = None
) -> list[sqlite3.Row]:
    """Return extra income entries for a month, optionally filtered by person."""
    query = """
        SELECT ei.id, ei.month_id, ei.person_id, ei.amount, ei.description,
               ei.date, p.name AS person_name
        FROM extra_income ei
        JOIN people p ON p.id = ei.person_id
        WHERE ei.month_id = ?
    """
    params: list = [month_id]
    if person_filter is not None:
        query += " AND ei.person_id = ?"
        params.append(person_filter)
    query += " ORDER BY ei.date DESC, ei.id DESC"
    return db.execute(query, params).fetchall()


def get_total_for_month(db: sqlite3.Connection, month_id: int) -> float:
    """Return total extra income for a month."""
    row = db.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM extra_income WHERE month_id = ?",
        (month_id,),
    ).fetchone()
    return row["total"]


def get_by_id(db: sqlite3.Connection, entry_id: int) -> sqlite3.Row | None:
    """Return a single extra income entry."""
    return db.execute(
        "SELECT * FROM extra_income WHERE id = ?", (entry_id,)
    ).fetchone()


def create(
    db: sqlite3.Connection,
    month_id: int,
    person_id: int,
    amount: float,
    description: str,
    entry_date: str,
) -> int:
    """Insert a new extra income entry."""
    cursor = db.execute(
        """
        INSERT INTO extra_income (month_id, person_id, amount, description, date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (month_id, person_id, amount, description, entry_date),
    )
    db.commit()
    return cursor.lastrowid


def delete(db: sqlite3.Connection, entry_id: int) -> None:
    """Delete an extra income entry."""
    db.execute("DELETE FROM extra_income WHERE id = ?", (entry_id,))
    db.commit()
