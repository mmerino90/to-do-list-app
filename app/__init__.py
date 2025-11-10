"""Application factory module."""
import os
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

from config.settings import config
from app.models.task import db
from app.api import tasks as tasks_api
from app.web import routes as web_routes
from app.utils.error_handlers import register_error_handlers

def create_app(config_name=None):
    """Create Flask application."""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")
    
    app = Flask(__name__,
                static_folder="../static",
                template_folder="../templates")
    
    # Load config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    PrometheusMetrics(app)
    
    # Register blueprints
    app.register_blueprint(tasks_api.bp)
    app.register_blueprint(web_routes.bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app