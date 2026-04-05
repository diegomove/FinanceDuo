"""Main routes: authentication, settings, service worker, language."""

from datetime import date
import secrets
from urllib.parse import urlparse

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.wrappers import Response

from models.db import get_db
from models.initial_balance import get_by_person, upsert as upsert_balance
from models.people import get_all, get_by_id, get_by_name, set_password, verify_password
from translations import (
    DEFAULT_LANG,
    LANGUAGES,
    MONTH_NAMES,
    get_translations,
    t,
)

bp = Blueprint("main", __name__)

ALLOWED_ROUTES = {"main.login", "main.login_post", "main.service_worker", "main.set_language", "static"}
STATE_CHANGING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def _lang() -> str:
    """Return current language from session."""
    return session.get("lang", DEFAULT_LANG)


def _csrf_token() -> str:
    """Get or create the CSRF token bound to the current session."""
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def _is_same_origin() -> bool:
    """Validate same-origin requests for state-changing methods."""
    host = urlparse(request.host_url)
    origin = request.headers.get("Origin")
    if origin:
        origin_parts = urlparse(origin)
        return origin_parts.scheme == host.scheme and origin_parts.netloc == host.netloc

    referer = request.headers.get("Referer")
    if referer:
        referer_parts = urlparse(referer)
        return referer_parts.scheme == host.scheme and referer_parts.netloc == host.netloc

    return False


def _safe_referrer_redirect(fallback_endpoint: str):
    """Redirect back only when the referrer belongs to this app origin."""
    referrer = request.referrer
    if referrer:
        host = urlparse(request.host_url)
        ref = urlparse(referrer)
        if ref.scheme == host.scheme and ref.netloc == host.netloc:
            return redirect(referrer)
    return redirect(url_for(fallback_endpoint))


@bp.before_app_request
def require_login() -> Response | None:
    """Redirect to login if not authenticated."""
    if request.endpoint not in ALLOWED_ROUTES and "person_id" not in session:
        return redirect(url_for("main.login"))
    return None


@bp.before_app_request
def protect_state_changing_requests() -> Response | None:
    """Apply CSRF and same-origin checks on unsafe HTTP methods."""
    if request.method not in STATE_CHANGING_METHODS:
        return None

    if not _is_same_origin():
        abort(403)

    token = request.form.get("_csrf_token") or request.headers.get("X-CSRF-Token")
    if token and token != session.get("csrf_token"):
        abort(400)

    return None


@bp.route("/sw.js")
def service_worker():
    """Serve the service worker from root scope."""
    return send_from_directory("static", "sw.js", mimetype="application/javascript")


@bp.app_context_processor
def inject_globals() -> dict:
    """Make current user, year, translations, and language available to all templates."""
    person_id: int | None = session.get("person_id")
    current_user = None
    if person_id is not None:
        db = get_db()
        current_user = get_by_id(db, person_id)
    lang = _lang()
    return {
        "current_user": current_user,
        "current_year": date.today().year,
        "t": get_translations(lang),
        "lang": lang,
        "LANGUAGES": LANGUAGES,
        "MONTH_NAMES_I18N": MONTH_NAMES.get(lang, MONTH_NAMES[DEFAULT_LANG]),
        "csrf_token": _csrf_token(),
    }


@bp.route("/")
def login():
    """Show login page or redirect to months if already logged in."""
    if "person_id" in session:
        return redirect(url_for("month.list_months"))
    db = get_db()
    people = get_all(db)
    return render_template("login.html", people=people)


@bp.route("/login", methods=["POST"])
def login_post():
    """Authenticate user."""
    name = request.form.get("name", "").strip()
    password = request.form.get("password", "")

    db = get_db()
    person = get_by_name(db, name)

    if person is None or not verify_password(db, person["id"], password):
        flash(t("wrong_credentials", _lang()), "danger")
        people = get_all(db)
        return render_template("login.html", people=people), 401

    session["person_id"] = person["id"]
    flash(t("welcome", _lang()).format(person["name"]), "success")
    return redirect(url_for("month.list_months"))


@bp.route("/set-language", methods=["POST"])
def set_language():
    """Set the UI language."""
    lang = request.form.get("lang", DEFAULT_LANG)
    if lang in LANGUAGES:
        session["lang"] = lang
    return _safe_referrer_redirect("main.login")


@bp.route("/logout")
def logout():
    """Log out and clear session."""
    lang = session.get("lang")
    session.clear()
    if lang:
        session["lang"] = lang
    return redirect(url_for("main.login"))


@bp.route("/switch-profile")
def switch_profile():
    """Log out and return to login."""
    lang = session.get("lang")
    session.clear()
    if lang:
        session["lang"] = lang
    return redirect(url_for("main.login"))


@bp.route("/settings")
def settings():
    """App settings page with initial balance and password change."""
    db = get_db()
    people = get_all(db)
    balances: dict[int, float] = {}
    for person in people:
        balances[person["id"]] = get_by_person(db, person["id"])
    return render_template("settings.html", people=people, balances=balances)


@bp.route("/settings/initial-balance", methods=["POST"])
def save_initial_balance():
    """Save initial bank balances."""
    person_id = session.get("person_id")
    if person_id is None:
        return redirect(url_for("main.login"))

    db = get_db()
    people = get_all(db)
    for person in people:
        amount_str = request.form.get(f"balance_{person['id']}", "0")
        try:
            amount = float(amount_str) if amount_str else 0.0
        except ValueError:
            amount = 0.0
        upsert_balance(db, person["id"], amount)

    flash(t("balances_saved", _lang()), "success")
    return redirect(url_for("main.settings"))


@bp.route("/settings/change-password", methods=["POST"])
def change_password():
    """Change the current user's password."""
    person_id = session.get("person_id")
    if person_id is None:
        return redirect(url_for("main.login"))

    current_pw = request.form.get("current_password", "")
    new_pw = request.form.get("new_password", "")
    confirm_pw = request.form.get("confirm_password", "")
    lang = _lang()

    db = get_db()

    if not verify_password(db, person_id, current_pw):
        flash(t("wrong_current_pw", lang), "danger")
        return redirect(url_for("main.settings"))

    if len(new_pw) < 8:
        flash(t("pw_min_length", lang), "danger")
        return redirect(url_for("main.settings"))

    if new_pw != confirm_pw:
        flash(t("pw_dont_match", lang), "danger")
        return redirect(url_for("main.settings"))

    set_password(db, person_id, new_pw)
    flash(t("pw_changed", lang), "success")
    return redirect(url_for("main.settings"))
