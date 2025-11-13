"""Application factory module.

This module handles Flask application creation and configuration,
following the Application Factory pattern for better testability
and modularity.
"""
import os
from flask import Flask
from config.settings import config


def _get_config_name() -> str:
    """Get the configuration name from environment variables.
    
    Priority order:
    1. FLASK_CONFIG environment variable
    2. FLASK_ENV environment variable
    3. Default to 'development'
    
    Returns:
        Configuration name string
    """
    return os.getenv("FLASK_CONFIG") or os.getenv("FLASK_ENV", "development")


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application.
    
    This is the main application factory that:
    - Loads configuration
    - Initializes extensions (database, metrics)
    - Registers blueprints
    - Registers error handlers
    - Creates database tables if needed
    
    Args:
        config_name: Configuration name (development/testing/production).
                    If None, determined from environment variables.
    
    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = _get_config_name()

    app = Flask(
        __name__,
        static_folder="../static",
        template_folder="../templates",
    )

    # Load configuration object
    _load_config(app, config_name)
    
    # Initialize database connection URL from environment
    _init_database_uri(app)
    
    # Security settings
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    
    # Log database connection status (without exposing secrets)
    app.logger.info(
        "DB URI present: %s", bool(app.config.get("SQLALCHEMY_DATABASE_URI"))
    )

    # Initialize extensions
    from app.extensions import db, metrics
    db.init_app(app)
    metrics.init_app(app)

    # Register blueprints
    _register_blueprints(app)
    
    # Register error handlers
    _register_error_handlers(app)
    
    # Create database tables in non-production environments
    _init_database(app)

    return app


def _load_config(app: Flask, config_name: str) -> None:
    """Load configuration from the config classes.
    
    Args:
        app: Flask application instance
        config_name: Configuration name to load
    """
    config_obj = config.get(config_name, config["development"])
    app.config.from_object(config_obj)
    config_obj.init_app(app)


def _init_database_uri(app: Flask) -> None:
    """Initialize database URI from environment variables.
    
    Normalizes PostgreSQL URIs for SQLAlchemy compatibility
    (handles Heroku-style postgres:// URLs).
    
    Args:
        app: Flask application instance
    """
    uri = _get_normalized_db_uri()
    if uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = uri


def _get_normalized_db_uri() -> str:
    """Get database URI from environment and normalize it for SQLAlchemy.
    
    NOTE: This should only be used for production (from Cloud Run env vars).
    For dev/test, the Config classes define their own URIs.
    
    Returns:
        Normalized database URI string, or empty string if not set
    """
    uri = os.getenv("SQLALCHEMY_DATABASE_URI", "")
    if not uri:
        return ""
    
    # Handle Heroku-style postgres:// URLs
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    # Ensure psycopg2 driver is specified
    if uri.startswith("postgresql://"):
        uri = uri.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    return uri


def _register_blueprints(app: Flask) -> None:
    """Register application blueprints.
    
    Args:
        app: Flask application instance
    """
    from app.api.tasks import bp as tasks_bp
    from app.web.routes import bp as web_bp

    app.register_blueprint(tasks_bp, url_prefix="/api/v1")
    app.register_blueprint(web_bp)  # UI at "/"


def _register_error_handlers(app: Flask) -> None:
    """Register error handlers and ping endpoint.
    
    Args:
        app: Flask application instance
    """
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    @app.route("/api/v1/ping", methods=["GET"])
    def ping():
        """Simple ping endpoint for health checks."""
        return {"message": "pong"}, 200


def _init_database(app: Flask) -> None:
    """Initialize database tables in non-production environments.
    
    Args:
        app: Flask application instance
    """
    config_name = _get_config_name()
    is_production = config_name == "production"
    
    if not is_production:
        with app.app_context():
            from app.extensions import db
            db.create_all()
