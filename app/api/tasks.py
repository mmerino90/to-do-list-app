"""API routes for tasks."""
from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate
from app.utils.error_handlers import NotFoundError

bp = Blueprint("api", __name__, url_prefix="/api/v1")

@bp.route("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

@bp.route("/tasks", methods=["GET"])
def get_tasks():
    """Get all tasks."""
    tasks = TaskService.get_all_tasks()
    return jsonify([task.to_dict() for task in tasks])

@bp.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    try:
        task_data = TaskCreate(**request.get_json())
        task = TaskService.create_task(task_data)
        return jsonify(task.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 422

@bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    """Get a specific task."""
    task = TaskService.get_task_by_id(task_id)
    if not task:
        raise NotFoundError(f"Task {task_id} not found")
    return jsonify(task.to_dict())

@bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id: int):
    """Update a task."""
    task = TaskService.get_task_by_id(task_id)
    if not task:
        raise NotFoundError(f"Task {task_id} not found")
    
    try:
        task_data = TaskUpdate(**request.get_json())
        updated_task = TaskService.update_task(task, task_data)
        return jsonify(updated_task.to_dict())
    except ValidationError as e:
        return jsonify({"error": str(e)}), 422

@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    """Delete a task."""
    task = TaskService.get_task_by_id(task_id)
    if not task:
        raise NotFoundError(f"Task {task_id} not found")
    
    TaskService.delete_task(task)
    return "", 204

@bp.route("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}