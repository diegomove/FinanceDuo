"""Expense template model: save and reuse common expenses."""

import sqlite3


def get_all(db: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return all expense templates."""
    return db.execute(
        """
        SELECT et.id, et.category_id, et.paid_by, et.amount, et.description,
               et.split_mode, et.custom_ratio_person1,
               c.name AS category_name, c.type AS category_type,
               p.name AS paid_by_name
        FROM expense_templates et
        JOIN categories c ON c.id = et.category_id
        JOIN people p ON p.id = et.paid_by
        ORDER BY et.description, c.name
        """,
    ).fetchall()


def create(
    db: sqlite3.Connection,
    category_id: int,
    paid_by: int,
    amount: float,
    description: str,
    split_mode: str = "50/50",
    custom_ratio_person1: float = 50.0,
) -> int:
    """Create a new expense template. Returns the new ID."""
    cursor = db.execute(
        """
        INSERT INTO expense_templates
            (category_id, paid_by, amount, description, split_mode, custom_ratio_person1)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (category_id, paid_by, amount, description, split_mode, custom_ratio_person1),
    )
    db.commit()
    return cursor.lastrowid


def delete(db: sqlite3.Connection, template_id: int) -> None:
    """Delete an expense template."""
    db.execute("DELETE FROM expense_templates WHERE id = ?", (template_id,))
    db.commit()


def get_by_id(db: sqlite3.Connection, template_id: int) -> sqlite3.Row | None:
    """Return a single template by ID."""
    return db.execute(
        """
        SELECT et.*, c.name AS category_name, p.name AS paid_by_name
        FROM expense_templates et
        JOIN categories c ON c.id = et.category_id
        JOIN people p ON p.id = et.paid_by
        WHERE et.id = ?
        """,
        (template_id,),
    ).fetchone()
