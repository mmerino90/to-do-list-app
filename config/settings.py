"""Application configuration module."""
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

# Load environment variables from .env file (ignored in production if not present)
load_dotenv()

# Base directory of the project (…/app/.. -> project root)
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG: bool = False
    TESTING: bool = False

    # Database (env wins; fallback to project-root/todo.db)
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{(BASE_DIR / 'todo.db').as_posix()}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @staticmethod
    def init_app(app: Any) -> None:
        """Hook for env-specific setup."""
        # Nothing for base; subclasses may extend.
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"


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

        # Avoid duplicate handlers if reloading
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
