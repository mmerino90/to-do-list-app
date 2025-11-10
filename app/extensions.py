"""Application extensions module.

Centralized place for Flask extension instances to avoid circular imports.
"""
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

db = SQLAlchemy()
metrics = PrometheusMetrics.for_app(None)
