from flask import Blueprint

bp = Blueprint("ping", __name__)


@bp.get("/ping")
def ping():
    return {"msg": "pong"}, 200
