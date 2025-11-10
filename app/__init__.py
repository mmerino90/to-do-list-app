"""Application factory module."""
import os
from flask import Flask
from config.settings import config  # your config dict

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

    # Import inside the factory to avoid circular imports
    from app.extensions import db, metrics
    db.init_app(app)
    metrics.init_app(app)

    # Blueprints (import here, then register)
    from app.api.tasks import bp as tasks_bp
    from app.web.routes import bp as web_bp
    # If you have health/metrics blueprints in app/ops:
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

    app.register_blueprint(tasks_bp, url_prefix="/api/v1")
    app.register_blueprint(web_bp, url_prefix="/ui")

    # Error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # DB tables
    with app.app_context():
        db.create_all()

    return app
