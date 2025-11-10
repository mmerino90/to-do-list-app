"""Application configuration module."""
import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration."""
    
    # Flask configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG: bool = False
    TESTING: bool = False
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'todo.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @staticmethod
    def init_app(app: Any) -> None:
        """Initialize application configuration."""
        pass


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration."""
    
    @classmethod
    def init_app(cls, app: Any) -> None:
        """Production-specific initialization."""
        Config.init_app(app)
        
        # Configure production-specific logging
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists("logs"):
            os.mkdir("logs")
            
        file_handler = RotatingFileHandler(
            "logs/todo.log",
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s "
            "[in %(pathname)s:%(lineno)d]"
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config: Dict[str, Config] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}