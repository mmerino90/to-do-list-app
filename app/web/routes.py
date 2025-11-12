"""Web routes for the UI."""
from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint("web", __name__)

@bp.route("/")
def index():
    """Render the main UI page."""
    return render_template("index.html")


