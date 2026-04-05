"""Budget model queries: income and expected expenses."""

import sqlite3


def get_income(db: sqlite3.Connection, month_id: int) -> list[sqlite3.Row]:
    """Return income entries for a month."""
    return db.execute(
        """
        SELECT i.id, i.person_id, i.amount, i.description, p.name AS person_name
        FROM income i
        JOIN people p ON p.id = i.person_id
        WHERE i.month_id = ?
        ORDER BY i.person_id
        """,
        (month_id,),
    ).fetchall()


def get_income_total(db: sqlite3.Connection, month_id: int) -> float:
    """Return total income for a month."""
    row = db.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM income WHERE month_id = ?",
        (month_id,),
    ).fetchone()
    return row["total"]


def upsert_income(
    db: sqlite3.Connection,
    month_id: int,
    person_id: int,
    amount: float,
    description: str = "",
) -> None:
    """Insert or update income for a person in a month."""
    db.execute(
        """
        INSERT INTO income (month_id, person_id, amount, description)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(month_id, person_id)
        DO UPDATE SET amount = excluded.amount, description = excluded.description
        """,
        (month_id, person_id, amount, description),
    )


def get_expected_expenses(db: sqlite3.Connection, month_id: int) -> list[sqlite3.Row]:
    """Return expected expenses for a month with category info."""
    return db.execute(
        """
        SELECT ee.id, ee.category_id, ee.amount, ee.notes, ee.paid_by,
               c.name AS category_name, c.type AS category_type
        FROM expected_expenses ee
        JOIN categories c ON c.id = ee.category_id
        WHERE ee.month_id = ?
        ORDER BY c.type, c.name
        """,
        (month_id,),
    ).fetchall()


def get_expected_total(db: sqlite3.Connection, month_id: int) -> float:
    """Return total expected expenses for a month."""
    row = db.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM expected_expenses WHERE month_id = ?",
        (month_id,),
    ).fetchone()
    return row["total"]


def upsert_expected(
    db: sqlite3.Connection,
    month_id: int,
    category_id: int,
    amount: float,
    notes: str = "",
    paid_by: str = "split",
) -> None:
    """Insert or update an expected expense."""
    db.execute(
        """
        INSERT INTO expected_expenses (month_id, category_id, amount, notes, paid_by)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(month_id, category_id)
        DO UPDATE SET amount = excluded.amount, notes = excluded.notes, paid_by = excluded.paid_by
        """,
        (month_id, category_id, amount, notes, paid_by),
    )


def delete_expected(db: sqlite3.Connection, month_id: int, category_id: int) -> None:
    """Remove an expected expense entry."""
    db.execute(
        "DELETE FROM expected_expenses WHERE month_id = ? AND category_id = ?",
        (month_id, category_id),
    )


def save_budget(
    db: sqlite3.Connection,
    month_id: int,
    income_data: list[dict],
    expense_data: list[dict],
) -> None:
    """Save the entire budget plan in one atomic transaction.

    Args:
        income_data: List of {person_id, amount, description}.
        expense_data: List of {category_id, amount, notes}.
    """
    try:
        for entry in income_data:
            if entry["amount"] > 0:
                upsert_income(
                    db, month_id, entry["person_id"], entry["amount"], entry.get("description", "")
                )
            else:
                db.execute(
                    "DELETE FROM income WHERE month_id = ? AND person_id = ?",
                    (month_id, entry["person_id"]),
                )

        for entry in expense_data:
            if entry["amount"] > 0:
                upsert_expected(
                    db, month_id, entry["category_id"], entry["amount"],
                    entry.get("notes", ""), entry.get("paid_by", "split"),
                )
            else:
                delete_expected(db, month_id, entry["category_id"])

        db.commit()
    except Exception:
        db.rollback()
        raise
