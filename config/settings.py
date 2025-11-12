"""Application configuration module."""
import os
from pathlib import Path
from typing import Any, Dict  
from dotenv import load_dotenv

# Load environment variables from .env file (ignored in production if not present)
load_dotenv()

# Base directory of the project (…/app/.. -> project root)
BASE_DIR = Path(__file__).resolve().parent.parent


def _normalize_db_url(raw: str | None) -> str | None:
    """Normalize database URLs (handles postgres:// → postgresql+psycopg2://)."""
    if not raw:
        return None
    url = raw
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://") and "+psycopg2" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG: bool = False
    TESTING: bool = False

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Database (unified)
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(
        os.getenv("SQLALCHEMY_DATABASE_URI") or os.getenv("DATABASE_URL")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app: Any) -> None:
        """Hook for env-specific setup."""
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(
        os.getenv(
            "SQLALCHEMY_DATABASE_URI",
            os.getenv(
                "DATABASE_URL",
                f"postgresql+psycopg2://postgres:{os.getenv('POSTGRES_PASSWORD', 'your_password')}@localhost:5432/todo",
            ),
        )
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app: Any) -> None:
        """Production-specific initialization."""
        super(ProductionConfig, cls).init_app(app)

        import logging
        from logging.handlers import RotatingFileHandler

        # Absolute logs dir under project root; safe even if it exists
        logs_dir = (BASE_DIR / "logs")
        logs_dir.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            logs_dir / "todo.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10,
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        ))
        file_handler.setLevel(logging.INFO)

        attached = any(isinstance(h, RotatingFileHandler) for h in app.logger.handlers)
        if not attached:
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Production logging configured")


config: Dict[str, type[Config]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
