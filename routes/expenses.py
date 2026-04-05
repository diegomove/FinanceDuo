"""Expense tracking routes."""

import csv
import io
from datetime import date

from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models.db import get_db
from models.budget import get_expected_expenses
from models.expenses import (
    calculate_balance,
    count_for_month,
    create,
    delete,
    get_actual_by_category,
    get_all_for_month,
    get_by_id,
    get_total_for_month,
    update,
)

EXPENSES_PER_PAGE = 25
from models.settlements import (
    create as create_settlement,
    delete as delete_settlement,
    get_all_for_month as get_settlements,
    get_by_id as get_settlement_by_id,
    get_total_for_month as get_settlement_total,
)
from models.templates import (
    get_all as get_all_templates,
    create as create_template,
    delete as delete_template,
    get_by_id as get_template_by_id,
)
from models.extra_income import (
    create as create_extra_income,
    delete as delete_extra_income,
    get_all_for_month as get_extra_income_for_month,
    get_by_id as get_extra_income_by_id,
    get_total_for_month as get_extra_income_total,
)
from models.categories import get_all as get_all_categories
from models.months import get_by_id as get_month, get_display_name
from models.people import get_all as get_all_people
from translations import DEFAULT_LANG, t

bp = Blueprint("expenses", __name__)
VALID_SPLIT_MODES = {"50/50", "person1_only", "person2_only", "custom", "personal"}


def _lang() -> str:
    return session.get("lang", DEFAULT_LANG)


@bp.route("/months/<int:month_id>/expenses")
def list_expenses(month_id: int):
    """List actual expenses for a month."""
    db = get_db()
    month = get_month(db, month_id)
    if month is None:
        flash(t("month_not_found", _lang()), "danger")
        return redirect(url_for("month.list_months"))

    # Filters and pagination
    category_filter = request.args.get("category", type=int)
    paid_by_filter = request.args.get("paid_by", type=int)
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1

    total_count = count_for_month(db, month_id, category_filter, paid_by_filter)
    total_pages = max(1, (total_count + EXPENSES_PER_PAGE - 1) // EXPENSES_PER_PAGE)
    if page > total_pages:
        page = total_pages

    expenses = get_all_for_month(db, month_id, category_filter, paid_by_filter, page, EXPENSES_PER_PAGE)
    total = get_total_for_month(db, month_id)
    categories = get_all_categories(db)
    people = get_all_people(db)
    extra_income = get_extra_income_for_month(db, month_id)
    extra_income_total = get_extra_income_total(db, month_id)
    templates = get_all_templates(db)

    # Budget alerts: categories exceeding 80% or 100%
    lang = _lang()
    budget_alerts: list[dict] = []
    expected = get_expected_expenses(db, month_id)
    actual_by_cat = get_actual_by_category(db, month_id)
    for entry in expected:
        if entry["amount"] > 0:
            actual_amt = actual_by_cat.get(entry["category_id"], {}).get("actual", 0)
            pct = (actual_amt / entry["amount"]) * 100
            budget_word = t("of_budget", lang)
            if pct >= 100:
                budget_alerts.append({
                    "name": entry["category_name"],
                    "pct": pct,
                    "level": "danger",
                    "msg": f"{entry['category_name']}: {pct:.0f}% {budget_word} ({actual_amt:.2f} / {entry['amount']:.2f} \u20ac)",
                })
            elif pct >= 80:
                budget_alerts.append({
                    "name": entry["category_name"],
                    "pct": pct,
                    "level": "warning",
                    "msg": f"{entry['category_name']}: {pct:.0f}% {budget_word} ({actual_amt:.2f} / {entry['amount']:.2f} \u20ac)",
                })

    return render_template(
        "expenses/list.html",
        month=month,
        display_name=get_display_name(month),
        expenses=expenses,
        total=total,
        categories=categories,
        people=people,
        category_filter=category_filter,
        paid_by_filter=paid_by_filter,
        extra_income=extra_income,
        extra_income_total=extra_income_total,
        templates=templates,
        budget_alerts=budget_alerts,
        page=page,
        total_pages=total_pages,
        total_count=total_count,
        today=date.today().isoformat(),
    )


@bp.route("/months/<int:month_id>/expenses/add", methods=["GET", "POST"])
def add_expense(month_id: int):
    """Add a new expense."""
    db = get_db()
    month = get_month(db, month_id)
    lang = _lang()
    if month is None:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("month.list_months"))

    if month["is_closed"]:
        flash(t("cant_add_closed", lang), "warning")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    categories = get_all_categories(db)
    people = get_all_people(db)
    category_ids = {cat["id"] for cat in categories}
    people_ids = {person["id"] for person in people}

    if request.method == "POST":
        category_id = request.form.get("category_id", type=int)
        paid_by = request.form.get("paid_by", type=int)
        amount_str = request.form.get("amount", "0")
        description = request.form.get("description", "").strip()
        expense_date = request.form.get("date", date.today().isoformat())
        split_mode = request.form.get("split_mode", "50/50")
        custom_ratio = request.form.get("custom_ratio_person1", "50", type=float)

        if split_mode not in VALID_SPLIT_MODES:
            split_mode = "50/50"
        if custom_ratio is None or custom_ratio < 0 or custom_ratio > 100:
            custom_ratio = 50.0

        try:
            amount = float(amount_str)
        except ValueError:
            amount = 0.0

        if (
            not category_id
            or not paid_by
            or amount <= 0
            or category_id not in category_ids
            or paid_by not in people_ids
        ):
            flash(t("fill_required", lang), "danger")
            return render_template(
                "expenses/add.html",
                month=month,
                display_name=get_display_name(month),
                categories=categories,
                people=people,
                edit=False,
            )

        create(db, month_id, category_id, paid_by, amount, description,
               expense_date, split_mode, custom_ratio)
        flash(t("expense_added", lang), "success")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    return render_template(
        "expenses/add.html",
        month=month,
        display_name=get_display_name(month),
        categories=categories,
        people=people,
        edit=False,
        today=date.today().isoformat(),
    )


@bp.route("/months/<int:month_id>/expenses/<int:expense_id>/edit", methods=["GET", "POST"])
def edit_expense(month_id: int, expense_id: int):
    """Edit an existing expense."""
    db = get_db()
    month = get_month(db, month_id)
    lang = _lang()
    if month is None:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("month.list_months"))

    expense = get_by_id(db, expense_id)
    if expense is None or expense["month_id"] != month_id:
        flash(t("expense_not_found", lang), "danger")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    if month["is_closed"]:
        flash(t("cant_edit_exp_closed", lang), "warning")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    categories = get_all_categories(db)
    people = get_all_people(db)
    category_ids = {cat["id"] for cat in categories}
    people_ids = {person["id"] for person in people}

    if request.method == "POST":
        category_id = request.form.get("category_id", type=int)
        paid_by = request.form.get("paid_by", type=int)
        amount_str = request.form.get("amount", "0")
        description = request.form.get("description", "").strip()
        expense_date = request.form.get("date", date.today().isoformat())
        split_mode = request.form.get("split_mode", "50/50")
        custom_ratio = request.form.get("custom_ratio_person1", "50", type=float)

        if split_mode not in VALID_SPLIT_MODES:
            split_mode = "50/50"
        if custom_ratio is None or custom_ratio < 0 or custom_ratio > 100:
            custom_ratio = 50.0

        try:
            amount = float(amount_str)
        except ValueError:
            amount = 0.0

        if (
            not category_id
            or not paid_by
            or amount <= 0
            or category_id not in category_ids
            or paid_by not in people_ids
        ):
            flash(t("fill_required", lang), "danger")
            return render_template(
                "expenses/add.html",
                month=month,
                display_name=get_display_name(month),
                categories=categories,
                people=people,
                expense=expense,
                edit=True,
            )

        update(db, expense_id, category_id, paid_by, amount, description,
               expense_date, split_mode, custom_ratio)
        flash(t("expense_updated", lang), "success")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    return render_template(
        "expenses/add.html",
        month=month,
        display_name=get_display_name(month),
        categories=categories,
        people=people,
        expense=expense,
        edit=True,
    )


@bp.route("/months/<int:month_id>/expenses/<int:expense_id>/delete", methods=["POST"])
def delete_expense(month_id: int, expense_id: int):
    """Delete an expense."""
    db = get_db()
    month = get_month(db, month_id)
    lang = _lang()

    if month is None:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("month.list_months"))

    if month["is_closed"]:
        flash(t("cant_delete_closed", lang), "warning")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    expense = get_by_id(db, expense_id)
    if expense is None or expense["month_id"] != month_id:
        flash(t("expense_not_found", lang), "danger")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    delete(db, expense_id)
    flash(t("expense_deleted", lang), "success")
    return redirect(url_for("expenses.list_expenses", month_id=month_id))


@bp.route("/months/<int:month_id>/extra-income/add", methods=["POST"])
def add_extra_income(month_id: int):
    """Add an extra income entry (Bizum, refund, etc.)."""
    db = get_db()
    month = get_month(db, month_id)
    lang = _lang()
    if month is None:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("month.list_months"))

    if month["is_closed"]:
        flash(t("cant_add_income_closed", lang), "warning")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    person_id = request.form.get("person_id", type=int)
    amount_str = request.form.get("amount", "0")
    description = request.form.get("description", "").strip()
    entry_date = request.form.get("date", date.today().isoformat())

    try:
        amount = float(amount_str)
    except ValueError:
        amount = 0.0

    people_ids = {p["id"] for p in get_all_people(db)}
    if not person_id or amount <= 0 or person_id not in people_ids:
        flash(t("fill_income_required", lang), "danger")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    create_extra_income(db, month_id, person_id, amount, description, entry_date)
    flash(t("extra_income_added", lang), "success")
    return redirect(url_for("expenses.list_expenses", month_id=month_id))


@bp.route("/months/<int:month_id>/extra-income/<int:entry_id>/delete", methods=["POST"])
def delete_extra_income_entry(month_id: int, entry_id: int):
    """Delete an extra income entry."""
    db = get_db()
    month = get_month(db, month_id)
    lang = _lang()

    if month is None:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("month.list_months"))

    if month["is_closed"]:
        flash(t("cant_delete_income_closed", lang), "warning")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    entry = get_extra_income_by_id(db, entry_id)
    if entry is None or entry["month_id"] != month_id:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    delete_extra_income(db, entry_id)
    flash(t("extra_income_deleted", lang), "success")
    return redirect(url_for("expenses.list_expenses", month_id=month_id))


@bp.route("/months/<int:month_id>/expenses/<int:expense_id>/save-template", methods=["POST"])
def save_as_template(month_id: int, expense_id: int):
    """Save an existing expense as a reusable template."""
    db = get_db()
    expense = get_by_id(db, expense_id)
    lang = _lang()
    if expense is None or expense["month_id"] != month_id:
        flash(t("expense_not_found", lang), "danger")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    create_template(
        db,
        expense["category_id"],
        expense["paid_by"],
        expense["amount"],
        expense["description"] or "",
        expense["split_mode"],
        expense["custom_ratio_person1"],
    )
    flash(t("template_saved", lang), "success")
    return redirect(url_for("expenses.list_expenses", month_id=month_id))


@bp.route("/months/<int:month_id>/templates/<int:template_id>/use", methods=["POST"])
def use_template(month_id: int, template_id: int):
    """Create a new expense from a template."""
    db = get_db()
    month = get_month(db, month_id)
    lang = _lang()
    if month is None or month["is_closed"]:
        flash(t("cant_add_this_month", lang), "warning")
        return redirect(url_for("month.list_months"))

    tmpl = get_template_by_id(db, template_id)
    if tmpl is None:
        flash(t("template_not_found", lang), "danger")
        return redirect(url_for("expenses.list_expenses", month_id=month_id))

    create(
        db, month_id, tmpl["category_id"], tmpl["paid_by"], tmpl["amount"],
        tmpl["description"] or "", date.today().isoformat(),
        tmpl["split_mode"], tmpl["custom_ratio_person1"],
    )
    flash(t("expense_from_template", lang), "success")
    return redirect(url_for("expenses.list_expenses", month_id=month_id))


@bp.route("/months/<int:month_id>/templates/<int:template_id>/delete", methods=["POST"])
def remove_template(month_id: int, template_id: int):
    """Delete an expense template."""
    db = get_db()
    delete_template(db, template_id)
    flash(t("template_deleted", _lang()), "success")
    return redirect(url_for("expenses.list_expenses", month_id=month_id))


@bp.route("/months/<int:month_id>/expenses/export")
def export_csv(month_id: int):
    """Export expenses for a month as CSV."""
    db = get_db()
    month = get_month(db, month_id)
    lang = _lang()
    if month is None:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("month.list_months"))

    expenses = get_all_for_month(db, month_id)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        t("csv_date", lang), t("csv_description", lang), t("csv_category", lang),
        t("csv_type", lang), t("csv_paid_by", lang), t("csv_split", lang), t("csv_amount", lang),
    ])
    for exp in expenses:
        writer.writerow([
            exp["date"],
            exp["description"] or "",
            exp["category_name"],
            exp["category_type"],
            exp["paid_by_name"],
            exp["split_mode"],
            f"{exp['amount']:.2f}",
        ])

    response = make_response(output.getvalue())
    display_name = get_display_name(month).replace(" ", "_")
    response.headers["Content-Disposition"] = f"attachment; filename=expenses_{display_name}.csv"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    return response


@bp.route("/months/<int:month_id>/balance")
def balance(month_id: int):
    """Show balance between the two people."""
    db = get_db()
    month = get_month(db, month_id)
    lang = _lang()
    if month is None:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("month.list_months"))

    balance_data = calculate_balance(db, month_id, lang)
    settlements = get_settlements(db, month_id)
    settlement_net = get_settlement_total(db, month_id)
    people = get_all_people(db)

    # Adjusted balance after settlements
    remaining = balance_data["net_amount"]
    if balance_data["debtor_id"] == 2:
        remaining = max(0, balance_data["net_amount"] - settlement_net)
    elif balance_data["debtor_id"] == 1:
        remaining = max(0, balance_data["net_amount"] + settlement_net)

    return render_template(
        "expenses/balance.html",
        month=month,
        display_name=get_display_name(month),
        balance=balance_data,
        settlements=settlements,
        settlement_net=settlement_net,
        remaining=remaining,
        people=people,
        today=date.today().isoformat(),
    )


@bp.route("/months/<int:month_id>/settlements/add", methods=["POST"])
def add_settlement(month_id: int):
    """Record a settlement payment."""
    db = get_db()
    month = get_month(db, month_id)
    lang = _lang()
    if month is None:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("month.list_months"))

    if month["is_closed"]:
        flash(t("cant_edit_closed", lang), "warning")
        return redirect(url_for("expenses.balance", month_id=month_id))

    paid_by = request.form.get("paid_by", type=int)
    paid_to = request.form.get("paid_to", type=int)
    amount_str = request.form.get("amount", "0")
    description = request.form.get("description", "").strip()
    settlement_date = request.form.get("date", date.today().isoformat())

    try:
        amount = float(amount_str)
    except ValueError:
        amount = 0.0

    people_ids = {p["id"] for p in get_all_people(db)}
    if (
        not paid_by
        or not paid_to
        or amount <= 0
        or paid_by == paid_to
        or paid_by not in people_ids
        or paid_to not in people_ids
    ):
        flash(t("settlement_invalid", lang), "danger")
        return redirect(url_for("expenses.balance", month_id=month_id))

    create_settlement(db, month_id, paid_by, paid_to, amount, description, settlement_date)
    flash(t("settlement_registered", lang), "success")
    return redirect(url_for("expenses.balance", month_id=month_id))


@bp.route("/months/<int:month_id>/settlements/<int:settlement_id>/delete", methods=["POST"])
def remove_settlement(month_id: int, settlement_id: int):
    """Delete a settlement."""
    db = get_db()
    month = get_month(db, month_id)
    lang = _lang()

    if month is None:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("month.list_months"))

    if month["is_closed"]:
        flash(t("cant_edit_closed", lang), "warning")
        return redirect(url_for("expenses.balance", month_id=month_id))

    settlement = get_settlement_by_id(db, settlement_id)
    if settlement is None or settlement["month_id"] != month_id:
        flash(t("month_not_found", lang), "danger")
        return redirect(url_for("expenses.balance", month_id=month_id))

    delete_settlement(db, settlement_id)
    flash(t("settlement_deleted", _lang()), "success")
    return redirect(url_for("expenses.balance", month_id=month_id))
