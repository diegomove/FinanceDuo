"""Blueprint registration."""

from flask import Flask


def register_blueprints(app: Flask) -> None:
    """Register all route blueprints with the app."""
    from routes.main import bp as main_bp
    from routes.month import bp as month_bp
    from routes.budget import bp as budget_bp
    from routes.expenses import bp as expenses_bp
    from routes.dashboard import bp as dashboard_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(month_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(dashboard_bp)
