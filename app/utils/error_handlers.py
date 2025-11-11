"""Error handlers and custom exceptions."""
from __future__ import annotations
from typing import Any, Dict, Optional, Tuple
from flask import jsonify, Response
from werkzeug.exceptions import UnprocessableEntity, NotFound, InternalServerError


class APIError(Exception):
    """Base API error with JSON payload."""
    status_code = 500

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> Dict[str, Any]:
        return {"error": self.message}


class NotFoundError(APIError):
    """Resource not found error."""
    status_code = 404


def register_error_handlers(app) -> None:
    """Register JSON error handlers for consistent API responses."""

    @app.errorhandler(APIError)
    def handle_api_error(error: APIError) -> Tuple[Response, int]:
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(404)
    def handle_404(error: NotFound) -> Tuple[Response, int]:
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(422)
    def handle_422(error: UnprocessableEntity) -> Tuple[Response, int]:
        return jsonify({"error": "Unprocessable entity"}), 422

    @app.errorhandler(500)
    def handle_500(error: InternalServerError) -> Tuple[Response, int]:
        return jsonify({"error": "Internal server error"}), 500