"""Test configuration."""
import os
import sys

import pytest

# Ensure project root is on sys.path so tests can import the `app` package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set testing config BEFORE importing app
os.environ["FLASK_CONFIG"] = "testing"
os.environ["FLASK_ENV"] = "testing"

from app import create_app  # noqa: E402
from app.extensions import db as _db  # noqa: E402


@pytest.fixture
def app():
    """Create application for the tests."""
    app = create_app("testing")
    # Ensure we're in testing mode
    app.config["TESTING"] = True
    return app


@pytest.fixture
def db(app):
    """Create database for the tests."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()
