"""Web routes for the UI."""
from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint("web", __name__)

@bp.route("/")
def index():
    """Render the main UI page."""
    return render_template("index.html")

# Optional convenience: allow /ui to work without trailing slash
@bp.route("", strict_slashes=False)
def ui_root():
    return redirect(url_for("web.index"))
