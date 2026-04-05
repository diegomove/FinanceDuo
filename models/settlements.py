"""Settlement model: track when debts are paid back."""

import sqlite3


def get_all_for_month(db: sqlite3.Connection, month_id: int) -> list[sqlite3.Row]:
    """Return all settlements for a month."""
    return db.execute(
        """
        SELECT s.id, s.month_id, s.paid_by, s.paid_to, s.amount,
               s.description, s.date, s.created_at,
               payer.name AS paid_by_name, receiver.name AS paid_to_name
        FROM settlements s
        JOIN people payer ON payer.id = s.paid_by
        JOIN people receiver ON receiver.id = s.paid_to
        WHERE s.month_id = ?
        ORDER BY s.date DESC
        """,
        (month_id,),
    ).fetchall()


def get_total_for_month(db: sqlite3.Connection, month_id: int) -> float:
    """Return net settlement amount for a month (positive = person1 paid person2)."""
    row = db.execute(
        """
        SELECT COALESCE(
            SUM(CASE WHEN paid_by = 1 THEN amount ELSE -amount END), 0
        ) AS net
        FROM settlements WHERE month_id = ?
        """,
        (month_id,),
    ).fetchone()
    return row["net"]


def get_by_id(db: sqlite3.Connection, settlement_id: int) -> sqlite3.Row | None:
    """Return a single settlement by ID."""
    return db.execute(
        "SELECT * FROM settlements WHERE id = ?",
        (settlement_id,),
    ).fetchone()


def create(
    db: sqlite3.Connection,
    month_id: int,
    paid_by: int,
    paid_to: int,
    amount: float,
    description: str,
    settlement_date: str,
) -> int:
    """Record a new settlement. Returns the new ID."""
    cursor = db.execute(
        """
        INSERT INTO settlements (month_id, paid_by, paid_to, amount, description, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (month_id, paid_by, paid_to, amount, description, settlement_date),
    )
    db.commit()
    return cursor.lastrowid


def delete(db: sqlite3.Connection, settlement_id: int) -> None:
    """Delete a settlement."""
    db.execute("DELETE FROM settlements WHERE id = ?", (settlement_id,))
    db.commit()
