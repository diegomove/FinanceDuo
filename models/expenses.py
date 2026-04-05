"""Actual expense model queries and balance calculations."""

import sqlite3
from datetime import date


def get_all_for_month(
    db: sqlite3.Connection,
    month_id: int,
    category_id: int | None = None,
    paid_by: int | None = None,
    page: int = 1,
    per_page: int = 0,
) -> list[sqlite3.Row]:
    """Return actual expenses for a month with optional filters and pagination.

    If per_page is 0, returns all results (no pagination).
    """
    query = """
        SELECT ae.id, ae.month_id, ae.category_id, ae.paid_by, ae.amount,
               ae.description, ae.date, ae.split_mode, ae.custom_ratio_person1,
               ae.created_at, c.name AS category_name, c.type AS category_type,
               p.name AS paid_by_name
        FROM actual_expenses ae
        JOIN categories c ON c.id = ae.category_id
        JOIN people p ON p.id = ae.paid_by
        WHERE ae.month_id = ?
    """
    params: list = [month_id]

    if category_id is not None:
        query += " AND ae.category_id = ?"
        params.append(category_id)

    if paid_by is not None:
        query += " AND ae.paid_by = ?"
        params.append(paid_by)

    query += " ORDER BY ae.date DESC, ae.created_at DESC"

    if per_page > 0:
        offset = (page - 1) * per_page
        query += " LIMIT ? OFFSET ?"
        params.extend([per_page, offset])

    return db.execute(query, params).fetchall()


def count_for_month(
    db: sqlite3.Connection,
    month_id: int,
    category_id: int | None = None,
    paid_by: int | None = None,
) -> int:
    """Count actual expenses for a month with optional filters."""
    query = "SELECT COUNT(*) AS cnt FROM actual_expenses WHERE month_id = ?"
    params: list = [month_id]

    if category_id is not None:
        query += " AND category_id = ?"
        params.append(category_id)

    if paid_by is not None:
        query += " AND paid_by = ?"
        params.append(paid_by)

    return db.execute(query, params).fetchone()["cnt"]


def get_by_id(db: sqlite3.Connection, expense_id: int) -> sqlite3.Row | None:
    """Return a single expense by ID."""
    return db.execute(
        """
        SELECT ae.*, c.name AS category_name, p.name AS paid_by_name
        FROM actual_expenses ae
        JOIN categories c ON c.id = ae.category_id
        JOIN people p ON p.id = ae.paid_by
        WHERE ae.id = ?
        """,
        (expense_id,),
    ).fetchone()


def create(
    db: sqlite3.Connection,
    month_id: int,
    category_id: int,
    paid_by: int,
    amount: float,
    description: str,
    expense_date: str,
    split_mode: str = "50/50",
    custom_ratio_person1: float = 50.0,
) -> int:
    """Insert a new expense. Returns the new ID."""
    cursor = db.execute(
        """
        INSERT INTO actual_expenses
            (month_id, category_id, paid_by, amount, description, date, split_mode, custom_ratio_person1)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (month_id, category_id, paid_by, amount, description, expense_date, split_mode, custom_ratio_person1),
    )
    db.commit()
    return cursor.lastrowid


def update(
    db: sqlite3.Connection,
    expense_id: int,
    category_id: int,
    paid_by: int,
    amount: float,
    description: str,
    expense_date: str,
    split_mode: str = "50/50",
    custom_ratio_person1: float = 50.0,
) -> None:
    """Update an existing expense."""
    db.execute(
        """
        UPDATE actual_expenses SET
            category_id = ?, paid_by = ?, amount = ?, description = ?,
            date = ?, split_mode = ?, custom_ratio_person1 = ?
        WHERE id = ?
        """,
        (category_id, paid_by, amount, description, expense_date, split_mode, custom_ratio_person1, expense_id),
    )
    db.commit()


def delete(db: sqlite3.Connection, expense_id: int) -> None:
    """Delete an expense."""
    db.execute("DELETE FROM actual_expenses WHERE id = ?", (expense_id,))
    db.commit()


def get_total_for_month(db: sqlite3.Connection, month_id: int) -> float:
    """Return total actual spending for a month."""
    row = db.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM actual_expenses WHERE month_id = ?",
        (month_id,),
    ).fetchone()
    return row["total"]


def get_actual_by_category(db: sqlite3.Connection, month_id: int) -> dict[int, dict]:
    """Return actual spending grouped by category for a month."""
    rows = db.execute(
        """
        SELECT c.id, c.name, c.type, COALESCE(SUM(ae.amount), 0) AS total
        FROM categories c
        LEFT JOIN actual_expenses ae ON ae.category_id = c.id AND ae.month_id = ?
        GROUP BY c.id
        ORDER BY c.type, c.name
        """,
        (month_id,),
    ).fetchall()
    return {
        row["id"]: {"name": row["name"], "type": row["type"], "actual": row["total"]}
        for row in rows
    }


def is_personal(expense: sqlite3.Row) -> bool:
    """Check if an expense is personal (non-shared)."""
    return expense["split_mode"] == "personal"


def compute_shares(expense: sqlite3.Row) -> tuple[float, float]:
    """Compute (person1_share, person2_share) for an expense.

    Returns:
        Tuple of (person1_share, person2_share) — how much each person should pay.
        Personal expenses return (amount, 0) or (0, amount) for the payer.
    """
    amount = expense["amount"]
    mode = expense["split_mode"]

    if mode == "personal":
        if expense["paid_by"] == 1:
            return amount, 0.0
        return 0.0, amount
    elif mode == "50/50":
        half = amount / 2
        return half, half
    elif mode == "person1_only":
        return amount, 0.0
    elif mode == "person2_only":
        return 0.0, amount
    elif mode == "custom":
        ratio = expense["custom_ratio_person1"] / 100.0
        return amount * ratio, amount * (1 - ratio)
    else:
        half = amount / 2
        return half, half


def get_personal_totals(db: sqlite3.Connection, month_id: int) -> dict[int, float]:
    """Return total personal spending per person for a month."""
    rows = db.execute(
        """
        SELECT paid_by, COALESCE(SUM(amount), 0) AS total
        FROM actual_expenses
        WHERE month_id = ? AND split_mode = 'personal'
        GROUP BY paid_by
        """,
        (month_id,),
    ).fetchall()
    return {row["paid_by"]: row["total"] for row in rows}


def calculate_balance(db: sqlite3.Connection, month_id: int, lang: str = "ca") -> dict:
    """Calculate the balance between person 1 and person 2 for a month.

    Personal expenses are tracked but excluded from the shared balance.

    Returns:
        Dict with balance details, person shares, and debtor info.
    """
    from translations import t as tr

    expenses = get_all_for_month(db, month_id)

    # Get person names for display
    people = db.execute("SELECT id, name FROM people ORDER BY id").fetchall()
    person1_name = people[0]["name"] if len(people) > 0 else "Person 1"
    person2_name = people[1]["name"] if len(people) > 1 else "Person 2"

    person1_paid_shared = 0.0
    person2_paid_shared = 0.0
    person1_should_pay = 0.0
    person2_should_pay = 0.0
    person1_personal = 0.0
    person2_personal = 0.0
    total_all = 0.0

    for exp in expenses:
        total_all += exp["amount"]

        if is_personal(exp):
            if exp["paid_by"] == 1:
                person1_personal += exp["amount"]
            else:
                person2_personal += exp["amount"]
            continue

        # Shared expense
        person1_share, person2_share = compute_shares(exp)

        if exp["paid_by"] == 1:
            person1_paid_shared += exp["amount"]
        else:
            person2_paid_shared += exp["amount"]

        person1_should_pay += person1_share
        person2_should_pay += person2_share

    # Person 1 overpaid by (what they paid - what they should pay)
    person1_balance = person1_paid_shared - person1_should_pay

    if person1_balance > 0:
        net_description = tr("owes_to", lang).format(person2_name, person1_name)
        net_amount = person1_balance
        debtor_id = 2
    elif person1_balance < 0:
        net_description = tr("owes_to", lang).format(person1_name, person2_name)
        net_amount = abs(person1_balance)
        debtor_id = 1
    else:
        net_description = tr("all_square", lang)
        net_amount = 0.0
        debtor_id = None

    return {
        "person1_paid": person1_paid_shared,
        "person2_paid": person2_paid_shared,
        "person1_should_pay": person1_should_pay,
        "person2_should_pay": person2_should_pay,
        "net_amount": net_amount,
        "net_description": net_description,
        "debtor_id": debtor_id,
        "total_shared": person1_paid_shared + person2_paid_shared,
        "person1_personal": person1_personal,
        "person2_personal": person2_personal,
        "person1_name": person1_name,
        "person2_name": person2_name,
        "total_all": total_all,
    }
