"""Application factory module."""
import os
from flask import Flask, redirect, url_for
from config.settings import config

def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(
        __name__,
        static_folder="../static",
        template_folder="../templates",
    )

    # Load config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Init extensions
    from app.extensions import db, metrics
    db.init_app(app)
    metrics.init_app(app)

    # Blueprints
    from app.api.tasks import bp as tasks_bp
    from app.web.routes import bp as web_bp
    app.register_blueprint(tasks_bp, url_prefix="/api/v1")
    app.register_blueprint(web_bp, url_prefix="/ui")

    # Optional ops blueprints
    try:
        from app.ops.health import bp as health_bp
        app.register_blueprint(health_bp, url_prefix="/api/v1")
    except Exception:
        pass
    try:
        from app.ops.metrics import bp as prom_metrics_bp
        app.register_blueprint(prom_metrics_bp, url_prefix="/api/v1")
    except Exception:
        pass

    # Root redirect: / -> /ui/
    def _root():
        return redirect(url_for("web.index"))
    app.add_url_rule("/", view_func=_root, endpoint="root", strict_slashes=False)

    # Error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # ✅ Simple ping route for CI/CD validation
    @app.route("/api/v1/ping", methods=["GET"])
    def ping():
        return {"message": "pong"}, 200

    # DB tables
    with app.app_context():
        db.create_all()

    return app
