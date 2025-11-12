"""Application factory module."""
import os
from flask import Flask
from config.settings import config


def _normalized_db_uri() -> str:
    """Get database URI from environment and normalize it for SQLAlchemy.

    NOTE: This should only be used for production (from Cloud Run env vars).
    For dev/test, the Config classes define their own URIs.
    """
    # Only use env vars if we have an explicitly set SQLALCHEMY_DATABASE_URI
    # (Cloud Run sets this). Ignore .env file DATABASE_URL in test/dev.
    uri = os.getenv("SQLALCHEMY_DATABASE_URI", "")
    if not uri:
        return ""
    # Heroku-style
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    # Force psycopg2 driver if not already set
    if uri.startswith("postgresql://"):
        uri = uri.replace("postgresql://", "postgresql+psycopg2://", 1)
    return uri


def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        # Accept FLASK_CONFIG or FLASK_ENV; Cloud Run typically uses FLASK_ENV
        config_name = os.getenv("FLASK_CONFIG") or os.getenv("FLASK_ENV", "development")

    app = Flask(
        __name__,
        static_folder="../static",
        template_folder="../templates",
    )

    # Load configuration object
    app.config.from_object(config.get(config_name, config["development"]))
    config[config_name if config_name in config else "development"].init_app(app)

    # Inject and normalize database URI from environment variables
    uri = _normalized_db_uri()
    if uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = uri

    # Security: disable ORM event spam
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # Useful logging for diagnostics without exposing secrets
    app.logger.info(
        "DB URI present: %s", bool(app.config.get("SQLALCHEMY_DATABASE_URI"))
    )

    from app.extensions import db, metrics

    db.init_app(app)
    metrics.init_app(app)

    # Register API and Web blueprints
    from app.api.tasks import bp as tasks_bp
    from app.web.routes import bp as web_bp

    app.register_blueprint(tasks_bp, url_prefix="/api/v1")
    app.register_blueprint(web_bp)  # UI at "/"

    from app.utils.error_handlers import register_error_handlers

    register_error_handlers(app)

    @app.route("/api/v1/ping", methods=["GET"])
    def ping():
        return {"message": "pong"}, 200

    if (
        os.getenv("FLASK_CONFIG") or os.getenv("FLASK_ENV", "development")
    ) != "production":
        with app.app_context():
            from app.extensions import db as _db

            _db.create_all()

    return app
