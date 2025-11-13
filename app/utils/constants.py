"""Constants for the application."""

# Database and timing
DUPLICATE_CHECK_WINDOW_SECONDS = 2  # Deduplication window for task creation

# HTTP Status Codes (defined as constants for clarity)
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_UNPROCESSABLE_ENTITY = 422
HTTP_INTERNAL_SERVER_ERROR = 500

# API Endpoints
API_PREFIX = "/api/v1"
ENDPOINT_TASKS = "/tasks"
ENDPOINT_TASKS_ID = "/tasks/<id>"
ENDPOINT_HEALTH = "/health"
ENDPOINT_METRICS = "/metrics"

# Error Messages
ERR_TASK_NOT_FOUND = "Task not found"
ERR_VALIDATION_FAILED = "Validation failed"
ERR_INTERNAL_ERROR = "Internal server error"
