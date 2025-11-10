"""Application factory module."""
import os
from flask import Flask, redirect, url_for

from config.settings import config
from app.extensions import db, metrics
from app.api import tasks as tasks_api
from app.web import routes as web_routes
from app.utils.error_handlers import register_error_handlers


def create_app(config_name=None):
    """Create Flask application."""
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

    # Initialize extensions
    db.init_app(app)
    metrics.init_app(app)

    # Register blueprints WITH PREFIXES
    app.register_blueprint(tasks_api.bp, url_prefix="/api/v1")
    app.register_blueprint(web_routes.bp, url_prefix="/ui")

    # Convenience: redirect root URL to the UI
    @app.route('/')
    def _root_redirect():
        return redirect(url_for('web.index'))

    # Register global error handlers
    register_error_handlers(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app