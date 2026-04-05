"""Budget planning routes."""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models.db import get_db
from models.budget import (
    get_expected_expenses,
    get_expected_total,
    get_income,
    get_income_total,
    save_budget,
)
from models.categories import get_grouped, create as create_category, get_all, update as update_category, delete as delete_category
from models.months import get_by_id, get_display_name
from models.people import get_all as get_all_people
from translations import DEFAULT_LANG, t

bp = Blueprint("budget", __name__)


def _lang() -> str:
    return session.get("lang", DEFAULT_LANG)


@bp.route("/months/<int:month_id>/budget")
def plan(month_id: int):
    """Budget planning page."""
    db = get_db()
    month = get_by_id(db, month_id)
    if month is None:
        flash(t("month_not_found", _lang()), "danger")
        return redirect(url_for("month.list_months"))

    people = get_all_people(db)
    categories = get_grouped(db)
    income_entries = get_income(db, month_id)
    expected = get_expected_expenses(db, month_id)

    # Build lookup dicts for template
    income_map: dict[int, dict] = {}
    for entry in income_entries:
        income_map[entry["person_id"]] = {
            "amount": entry["amount"],
            "description": entry["description"],
        }

    expected_map: dict[int, dict] = {}
    for entry in expected:
        expected_map[entry["category_id"]] = {
            "amount": entry["amount"],
            "notes": entry["notes"],
            "paid_by": entry["paid_by"],
        }

    income_total = get_income_total(db, month_id)
    expected_total = get_expected_total(db, month_id)

    return render_template(
        "budget/plan.html",
        month=month,
        display_name=get_display_name(month),
        people=people,
        categories=categories,
        income_map=income_map,
        expected_map=expected_map,
        income_total=income_total,
        expected_total=expected_total,
        surplus=income_total - expected_total,
    )


@bp.route("/months/<int:month_id>/budget", methods=["POST"])
def save_plan(month_id: int):
    """Save budget plan."""
    db = get_db()
    month = get_by_id(db, month_id)
    lang = _lang()
    if month is None:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("month.list_months"))

    if month["is_closed"]:
        flash(t("cant_edit_closed", lang), "warning")
        return redirect(url_for("budget.plan", month_id=month_id))

    people = get_all_people(db)
    all_categories = get_all(db)

    # Parse income
    income_data: list[dict] = []
    for person in people:
        amount_str = request.form.get(f"income_{person['id']}", "0")
        desc = request.form.get(f"income_desc_{person['id']}", "")
        try:
            amount = float(amount_str) if amount_str else 0.0
        except ValueError:
            amount = 0.0
        income_data.append({
            "person_id": person["id"],
            "amount": amount,
            "description": desc,
        })

    # Parse expected expenses
    expense_data: list[dict] = []
    for cat in all_categories:
        amount_str = request.form.get(f"expense_{cat['id']}", "0")
        notes = request.form.get(f"expense_notes_{cat['id']}", "")
        paid_by = request.form.get(f"expense_paidby_{cat['id']}", "split")
        if paid_by not in ("split", "person1", "person2", "personal_person1", "personal_person2"):
            paid_by = "split"
        try:
            amount = float(amount_str) if amount_str else 0.0
        except ValueError:
            amount = 0.0
        expense_data.append({
            "category_id": cat["id"],
            "amount": amount,
            "notes": notes,
            "paid_by": paid_by,
        })

    save_budget(db, month_id, income_data, expense_data)
    flash(t("budget_saved", lang), "success")
    return redirect(url_for("budget.plan", month_id=month_id))


@bp.route("/categories")
def manage_categories():
    """Category management page."""
    db = get_db()
    categories = get_grouped(db)
    return render_template("budget/categories.html", categories=categories)


@bp.route("/categories/add", methods=["POST"])
def add_category():
    """Add a new category."""
    name = request.form.get("name", "").strip()
    cat_type = request.form.get("type", "extra")
    lang = _lang()

    if not name:
        flash(t("cat_name_required", lang), "danger")
        return redirect(url_for("budget.manage_categories"))

    if cat_type not in ("fixed", "variable", "extra"):
        flash(t("cat_type_invalid", lang), "danger")
        return redirect(url_for("budget.manage_categories"))

    db = get_db()
    result = create_category(db, name, cat_type)
    if result is None:
        flash(t("cat_exists", lang), "warning")
    else:
        flash(t("cat_added", lang).format(name), "success")

    return redirect(url_for("budget.manage_categories"))


@bp.route("/categories/<int:cat_id>/edit", methods=["POST"])
def edit_category(cat_id: int):
    """Edit a category."""
    name = request.form.get("name", "").strip()
    cat_type = request.form.get("type", "extra")
    lang = _lang()

    if not name:
        flash(t("cat_name_required", lang), "danger")
        return redirect(url_for("budget.manage_categories"))

    db = get_db()
    success = update_category(db, cat_id, name, cat_type)
    if not success:
        flash(t("cat_exists", lang), "warning")
    else:
        flash(t("cat_updated", lang), "success")

    return redirect(url_for("budget.manage_categories"))


@bp.route("/categories/<int:cat_id>/delete", methods=["POST"])
def remove_category(cat_id: int):
    """Delete a category."""
    db = get_db()
    lang = _lang()
    if not delete_category(db, cat_id):
        flash(t("cat_in_use", lang), "warning")
    else:
        flash(t("cat_deleted", lang), "success")
    return redirect(url_for("budget.manage_categories"))
