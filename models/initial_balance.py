"""Initial balance model queries."""

import sqlite3


def get_all(db: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return initial balances for all people."""
    return db.execute(
        """
        SELECT ib.id, ib.person_id, ib.amount, p.name AS person_name
        FROM initial_balance ib
        JOIN people p ON p.id = ib.person_id
        ORDER BY ib.person_id
        """,
    ).fetchall()


def get_by_person(db: sqlite3.Connection, person_id: int) -> float:
    """Return the initial balance for a person (0 if not set)."""
    row = db.execute(
        "SELECT amount FROM initial_balance WHERE person_id = ?",
        (person_id,),
    ).fetchone()
    return row["amount"] if row else 0.0


def get_total(db: sqlite3.Connection) -> float:
    """Return the combined initial balance."""
    row = db.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM initial_balance"
    ).fetchone()
    return row["total"]


def upsert(db: sqlite3.Connection, person_id: int, amount: float) -> None:
    """Set the initial balance for a person."""
    db.execute(
        """
        INSERT INTO initial_balance (person_id, amount)
        VALUES (?, ?)
        ON CONFLICT(person_id)
        DO UPDATE SET amount = excluded.amount
        """,
        (person_id, amount),
    )
    db.commit()
