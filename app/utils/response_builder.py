"""Response builder for consistent HTTP responses."""
from typing import Any, Dict, Tuple, Optional
from flask import jsonify, Response


class ResponseBuilder:
    """Builder for consistent HTTP API responses."""

    @staticmethod
    def success(
        data: Any = None,
        status_code: int = 200,
        message: Optional[str] = None
    ) -> Tuple[Response, int]:
        """Build a successful response.
        
        Args:
            data: Response payload
            status_code: HTTP status code (default 200)
            message: Optional success message
            
        Returns:
            Flask response tuple (response, status_code)
        """
        if data is None and message is None:
            return "", status_code
        
        response_body: Dict[str, Any] = {}
        if message:
            response_body["message"] = message
        if data is not None:
            response_body["data"] = data
            
        return jsonify(response_body), status_code

    @staticmethod
    def error(
        message: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None
    ) -> Tuple[Response, int]:
        """Build an error response.
        
        Args:
            message: Error message
            status_code: HTTP status code (default 400)
            details: Optional error details
            
        Returns:
            Flask response tuple (response, status_code)
        """
        response_body: Dict[str, Any] = {"error": message}
        if details:
            response_body["details"] = details
            
        return jsonify(response_body), status_code

    @staticmethod
    def created(data: Any) -> Tuple[Response, int]:
        """Build a 201 Created response.
        
        Args:
            data: Created resource data
            
        Returns:
            Flask response tuple (response, 201)
        """
        return ResponseBuilder.success(data, 201)

    @staticmethod
    def not_found(message: str = "Resource not found") -> Tuple[Response, int]:
        """Build a 404 Not Found response.
        
        Args:
            message: Error message
            
        Returns:
            Flask response tuple (response, 404)
        """
        return ResponseBuilder.error(message, 404)

    @staticmethod
    def validation_error(message: str) -> Tuple[Response, int]:
        """Build a 422 Unprocessable Entity response.
        
        Args:
            message: Validation error message
            
        Returns:
            Flask response tuple (response, 422)
        """
        return ResponseBuilder.error(message, 422)

    @staticmethod
    def server_error(message: str = "Internal server error") -> Tuple[Response, int]:
        """Build a 500 Internal Server Error response.
        
        Args:
            message: Error message
            
        Returns:
            Flask response tuple (response, 500)
        """
        return ResponseBuilder.error(message, 500)
