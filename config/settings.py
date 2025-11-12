"""Application configuration module."""
import os
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def _get_database_uri() -> str:
    """
    Normalize the database URL:
    - Use SQLALCHEMY_DATABASE_URI if it exists
    - Otherwise use DATABASE_URL
    - Adjust postgresql scheme to postgresql+psycopg2 if needed
    """
    url = os.getenv("SQLALCHEMY_DATABASE_URI") or os.getenv("DATABASE_URL", "")
    if not url:
        return ""
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG: bool = False
    TESTING: bool = False

    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @staticmethod
    def init_app(app: Any) -> None:
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = _get_database_uri() or (
        f"postgresql+psycopg2://postgres:{os.getenv('POSTGRES_PASSWORD', 'your_password')}@localhost:5432/todo"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    # Database URI will be set dynamically in __init__.py to ensure env vars are loaded
    # Optionally harden the pool (prevents timeouts)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    @classmethod
    def init_app(cls, app: Any) -> None:
        super(ProductionConfig, cls).init_app(app)

        import logging
        from logging.handlers import RotatingFileHandler

        logs_dir = (BASE_DIR / "logs")
        logs_dir.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            logs_dir / "todo.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=10,
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        ))
        file_handler.setLevel(logging.INFO)

        if not any(isinstance(h, RotatingFileHandler) for h in app.logger.handlers):
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Production logging configured")


config: Dict[str, type[Config]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
