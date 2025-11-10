"""Web routes for the UI."""
from flask import Blueprint, render_template

bp = Blueprint("web", __name__)

@bp.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")