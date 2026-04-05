"""Bank balance calculations — current real money per person."""

import sqlite3

from models.initial_balance import get_by_person as get_initial


def get_current_balance(db: sqlite3.Connection, person_id: int) -> dict:
    """Calculate current bank balance for a person.

    Formula: initial_balance + total_income - total_paid_out_of_pocket
    Only uses actual expenses, not budget estimates.
    """
    initial = get_initial(db, person_id)

    row = db.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM income WHERE person_id = ?",
        (person_id,),
    ).fetchone()
    salary_income = row["total"]

    row = db.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM extra_income WHERE person_id = ?",
        (person_id,),
    ).fetchone()
    extra_income = row["total"]

    total_income = salary_income + extra_income

    row = db.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM actual_expenses WHERE paid_by = ?",
        (person_id,),
    ).fetchone()
    total_paid = row["total"]

    balance = initial + total_income - total_paid

    return {
        "initial": initial,
        "total_income": total_income,
        "total_paid": total_paid,
        "balance": balance,
    }
