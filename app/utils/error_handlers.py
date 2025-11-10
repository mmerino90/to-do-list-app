"""Error handlers and custom exceptions."""
from typing import Tuple, Dict, Any

from flask import jsonify


class APIError(Exception):
    """Base API error."""
    
    status_code = 500
    
    def __init__(self, message: str, status_code: int = None) -> None:
        """Initialize the error."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary."""
        return {"error": self.message}


class NotFoundError(APIError):
    """Resource not found error."""
    
    status_code = 404


def register_error_handlers(app):
    """Register error handlers with the Flask app."""
    
    @app.errorhandler(APIError)
    def handle_api_error(error: APIError) -> Tuple[Dict[str, Any], int]:
        """Handle API errors."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(404)
    def not_found_error(error) -> Tuple[Dict[str, str], int]:
        """Handle 404 errors."""
        return {"error": "Resource not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error) -> Tuple[Dict[str, str], int]:
        """Handle 500 errors."""
        return {"error": "Internal server error"}, 500