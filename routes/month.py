"""Month management routes."""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models.bank_balance import get_current_balance
from models.db import get_db
from models.months import (
    copy_fixed_expenses,
    create,
    get_all,
    get_by_id,
    get_current_year_month,
    get_display_name,
    get_month_summary,
    get_previous,
    toggle_closed,
)
from translations import DEFAULT_LANG, t

bp = Blueprint("month", __name__, url_prefix="/months")


def _lang() -> str:
    return session.get("lang", DEFAULT_LANG)


@bp.route("/")
def list_months():
    """List all months."""
    db = get_db()
    months = get_all(db)
    current_year, current_month = get_current_year_month()
    people = db.execute("SELECT id, name FROM people ORDER BY id").fetchall()
    person_balances = {p["id"]: get_current_balance(db, p["id"]) for p in people}

    summaries: dict[int, dict] = {}
    for m in months:
        summaries[m["id"]] = get_month_summary(db, m["id"])

    return render_template(
        "month/list.html",
        months=months,
        get_display_name=get_display_name,
        current_year=current_year,
        current_month=current_month,
        people=people,
        person_balances=person_balances,
        summaries=summaries,
    )


@bp.route("/create", methods=["POST"])
def create_month():
    """Create a new month."""
    year = request.form.get("year", type=int)
    month = request.form.get("month", type=int)

    if not year or not month or month < 1 or month > 12:
        flash(t("month_invalid", _lang()), "danger")
        return redirect(url_for("month.list_months"))

    db = get_db()
    month_id = create(db, year, month)

    if month_id is None:
        flash(t("month_exists", _lang()), "warning")
    else:
        flash(t("month_created", _lang()), "success")
        return redirect(url_for("month.overview", month_id=month_id))

    return redirect(url_for("month.list_months"))


@bp.route("/<int:month_id>")
def overview(month_id: int):
    """Month overview hub."""
    db = get_db()
    month = get_by_id(db, month_id)

    if month is None:
        flash(t("month_not_found", _lang()), "danger")
        return redirect(url_for("month.list_months"))

    previous = get_previous(db, month_id)

    return render_template(
        "month/overview.html",
        month=month,
        display_name=get_display_name(month),
        previous=previous,
    )


@bp.route("/<int:month_id>/close", methods=["POST"])
def close_month(month_id: int):
    """Toggle month closed status."""
    db = get_db()
    month = get_by_id(db, month_id)

    if month is None:
        flash(t("month_not_found", _lang()), "danger")
        return redirect(url_for("month.list_months"))

    lang = _lang()
    toggle_closed(db, month_id)
    msg_key = "month_reopened" if month["is_closed"] else "month_closed_action"
    flash(t(msg_key, lang), "success")
    return redirect(url_for("month.overview", month_id=month_id))


@bp.route("/<int:month_id>/copy-from/<int:source_id>", methods=["POST"])
def copy_budget(month_id: int, source_id: int):
    """Copy fixed expenses from source month."""
    db = get_db()
    count = copy_fixed_expenses(db, source_id, month_id)
    flash(t("fixed_copied", _lang()).format(count), "success")
    return redirect(url_for("month.overview", month_id=month_id))
