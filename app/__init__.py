"""Application factory module."""
import os
from flask import Flask, redirect, url_for
from config.settings import config

def create_app(config_name: str | None = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config_name (str | None): The configuration environment name (development, testing, production).
    
    Returns:
        app (Flask): The configured Flask application instance.
    """
    
    # Set the configuration to the environment variable or default to development
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    # Initialize the Flask application
    app = Flask(
        __name__,
        static_folder="../static",
        template_folder="../templates",
    )

    # Load the selected configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions (e.g., Database, Metrics)
    from app.extensions import db, metrics
    db.init_app(app)
    metrics.init_app(app)

    # Register API and web blueprints
    from app.api.tasks import bp as tasks_bp
    from app.web.routes import bp as web_bp
    app.register_blueprint(tasks_bp, url_prefix="/api/v1")
    app.register_blueprint(web_bp, url_prefix="/ui")

    # Optionally register health and metrics blueprints if present
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

    # Root redirect: Redirect root (/) to /ui/
    def _root():
        return redirect(url_for("web.index"))
    app.add_url_rule("/", view_func=_root, endpoint="root", strict_slashes=False)

    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Simple ping route for CI/CD validation
    @app.route("/api/v1/ping", methods=["GET"])
    def ping():
        """
        Simple endpoint for CI/CD validation to ensure the app is running.
        """
        return {"message": "pong"}, 200

    # Create database tables if they don't exist yet
    with app.app_context():
        db.create_all()

    return app