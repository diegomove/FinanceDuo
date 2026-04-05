"""Dashboard routes: expected vs actual comparison and charts."""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    session,
    url_for,
)

from models.db import get_db
from models.budget import get_expected_expenses, get_expected_total, get_income_total
from models.expenses import calculate_balance, get_actual_by_category, get_total_for_month
from models.extra_income import get_total_for_month as get_extra_income_total
from models.initial_balance import get_total as get_initial_balance_total
from models.months import get_all, get_by_id, get_display_name, get_month_summary
from translations import DEFAULT_LANG, t

bp = Blueprint("dashboard", __name__)


def _lang() -> str:
    return session.get("lang", DEFAULT_LANG)


@bp.route("/months/<int:month_id>/dashboard")
def comparison(month_id: int):
    """Expected vs actual comparison dashboard."""
    db = get_db()
    month = get_by_id(db, month_id)
    lang = _lang()
    if month is None:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("month.list_months"))

    # Expected data
    expected_entries = get_expected_expenses(db, month_id)
    expected_total = get_expected_total(db, month_id)
    income_total = get_income_total(db, month_id) + get_extra_income_total(db, month_id)

    # Actual data: sum per category
    actual_by_category = get_actual_by_category(db, month_id)

    # Build comparison data
    comparison_data: list[dict] = []
    expected_map: dict[int, float] = {}
    for entry in expected_entries:
        expected_map[entry["category_id"]] = entry["amount"]

    # Get all categories that have either expected or actual values
    all_cat_ids = set(expected_map.keys()) | {
        cid for cid, data in actual_by_category.items() if data["actual"] > 0
    }

    for cat_id in all_cat_ids:
        cat_info = actual_by_category.get(cat_id, {})
        expected_amt = expected_map.get(cat_id, 0.0)
        actual_amt = cat_info.get("actual", 0.0)
        diff = actual_amt - expected_amt

        comparison_data.append({
            "category_id": cat_id,
            "category_name": cat_info.get("name", "Unknown"),
            "category_type": cat_info.get("type", "extra"),
            "expected": expected_amt,
            "actual": actual_amt,
            "diff": diff,
            "status": "over" if diff > 0 else ("under" if diff < 0 else "on_target"),
        })

    comparison_data.sort(key=lambda x: (x["category_type"], x["category_name"]))

    # Totals
    actual_total = get_total_for_month(db, month_id)
    balance_data = calculate_balance(db, month_id, lang)
    initial_balance = get_initial_balance_total(db)
    savings = income_total - actual_total
    budget_used_pct = (actual_total / expected_total * 100) if expected_total > 0 else 0

    # Chart data
    chart_labels = [c["category_name"] for c in comparison_data if c["expected"] > 0 or c["actual"] > 0]
    chart_expected = [c["expected"] for c in comparison_data if c["expected"] > 0 or c["actual"] > 0]
    chart_actual = [c["actual"] for c in comparison_data if c["expected"] > 0 or c["actual"] > 0]

    # Pie data: only categories with actual spending
    pie_labels = [c["category_name"] for c in comparison_data if c["actual"] > 0]
    pie_values = [c["actual"] for c in comparison_data if c["actual"] > 0]

    chart_data = {
        "bar": {"labels": chart_labels, "expected": chart_expected, "actual": chart_actual},
        "pie": {"labels": pie_labels, "values": pie_values},
    }

    return render_template(
        "dashboard/comparison.html",
        month=month,
        display_name=get_display_name(month),
        comparison=comparison_data,
        income_total=income_total,
        expected_total=expected_total,
        actual_total=actual_total,
        savings=savings,
        initial_balance=initial_balance,
        budget_used_pct=budget_used_pct,
        balance=balance_data,
        chart_data=chart_data,
    )


@bp.route("/trends")
def trends():
    """Multi-month spending trends."""
    db = get_db()
    months = get_all(db)
    lang = _lang()

    if not months:
        flash(t("no_months_data", lang), "info")
        return redirect(url_for("month.list_months"))

    # Reverse to chronological order
    months_chronological = list(reversed(months))

    labels: list[str] = []
    income_data: list[float] = []
    budgeted_data: list[float] = []
    actual_data: list[float] = []
    savings_data: list[float] = []

    for m in months_chronological:
        summary = get_month_summary(db, m["id"])
        labels.append(get_display_name(m))
        income_data.append(summary["income"])
        budgeted_data.append(summary["budgeted"])
        actual_data.append(summary["actual"])
        savings_data.append(summary["income"] - summary["actual"])

    chart_data = {
        "labels": labels,
        "income": income_data,
        "budgeted": budgeted_data,
        "actual": actual_data,
        "savings": savings_data,
    }

    return render_template(
        "dashboard/trends.html",
        chart_data=chart_data,
        months=months_chronological,
        labels=labels,
        income_data=income_data,
        budgeted_data=budgeted_data,
        actual_data=actual_data,
        savings_data=savings_data,
    )
