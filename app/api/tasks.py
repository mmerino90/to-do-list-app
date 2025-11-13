"""API routes for tasks."""
from flask import Blueprint, request
from pydantic import ValidationError
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate
from app.utils.response_builder import ResponseBuilder
from app.utils.constants import (
    HTTP_OK, HTTP_CREATED, HTTP_NO_CONTENT, 
    HTTP_UNPROCESSABLE_ENTITY, HTTP_NOT_FOUND, HTTP_INTERNAL_SERVER_ERROR,
    ERR_TASK_NOT_FOUND, ERR_VALIDATION_FAILED, ERR_INTERNAL_ERROR
)
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

bp = Blueprint("api", __name__, url_prefix="/api/v1")


def _parse_request_json(schema_class):
    """Parse and validate request JSON against schema.
    
    Args:
        schema_class: Pydantic schema class for validation
        
    Returns:
        Tuple of (parsed_data, error_response) where one will be None
    """
    try:
        data = schema_class(**request.get_json() or {})
        return data, None
    except ValidationError as e:
        return None, ResponseBuilder.validation_error(str(e))


@bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint.
    
    Returns:
        JSON response with health status
    """
    return ResponseBuilder.success({"status": "healthy"})


@bp.route("/tasks", methods=["GET"])
def get_tasks():
    """Get all tasks.
    
    Returns:
        List of all tasks as JSON
    """
    try:
        tasks = TaskService.get_all_tasks()
        task_dicts = [task.to_dict() for task in tasks]
        return ResponseBuilder.success(task_dicts, HTTP_OK)
    except Exception as e:
        return ResponseBuilder.server_error(f"{ERR_INTERNAL_ERROR}: {str(e)}")


@bp.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task.
    
    Returns:
        Created task as JSON (201) or error response
    """
    try:
        # Parse and validate request
        task_data, error_response = _parse_request_json(TaskCreate)
        if error_response:
            return error_response
            
        # Create task
        task = TaskService.create_task(task_data)
        return ResponseBuilder.created(task.to_dict())
    except Exception as e:
        return ResponseBuilder.server_error(f"{ERR_INTERNAL_ERROR}: {str(e)}")


@bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    """Get a specific task by ID.
    
    Args:
        task_id: Task ID
        
    Returns:
        Task as JSON or 404 error
    """
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return ResponseBuilder.not_found(f"{ERR_TASK_NOT_FOUND}: {task_id}")
        return ResponseBuilder.success(task.to_dict(), HTTP_OK)
    except Exception as e:
        return ResponseBuilder.server_error(f"{ERR_INTERNAL_ERROR}: {str(e)}")


@bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id: int):
    """Update a specific task by ID.
    
    Args:
        task_id: Task ID
        
    Returns:
        Updated task as JSON or error response
    """
    try:
        # Check if task exists
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return ResponseBuilder.not_found(f"{ERR_TASK_NOT_FOUND}: {task_id}")
        
        # Parse and validate request
        task_data, error_response = _parse_request_json(TaskUpdate)
        if error_response:
            return error_response
            
        # Update task
        updated_task = TaskService.update_task(task, task_data)
        return ResponseBuilder.success(updated_task.to_dict(), HTTP_OK)
    except Exception as e:
        return ResponseBuilder.server_error(f"{ERR_INTERNAL_ERROR}: {str(e)}")


@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    """Delete a specific task by ID.
    
    Args:
        task_id: Task ID
        
    Returns:
        Empty response (204) or error response
    """
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return ResponseBuilder.not_found(f"{ERR_TASK_NOT_FOUND}: {task_id}")
        TaskService.delete_task(task)
        return "", HTTP_NO_CONTENT
    except Exception as e:
        return ResponseBuilder.server_error(f"{ERR_INTERNAL_ERROR}: {str(e)}")


@bp.route("/metrics", methods=["GET"])
def metrics():
    """Prometheus metrics endpoint.
    
    Returns:
        Prometheus metrics in text format
    """
    return generate_latest(), HTTP_OK, {"Content-Type": CONTENT_TYPE_LATEST}
