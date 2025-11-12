"""API routes for tasks."""
from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

bp = Blueprint("api", __name__, url_prefix="/api/v1")

# Metrics definitions
REQUEST_COUNT = Counter(
    "todo_api_request_count",
    "Total number of requests",
    ["method", "endpoint", "http_status"],
)
REQUEST_LATENCY = Histogram(
    "todo_api_request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
)
ERROR_COUNT = Counter(
    "todo_api_error_count",
    "Total number of errors",
    ["method", "endpoint", "http_status"],
)


@bp.route("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@bp.route("/tasks", methods=["GET"])
def get_tasks():
    start_time = time.time()
    try:
        tasks = TaskService.get_all_tasks()
        status = 200
        return jsonify([task.to_dict() for task in tasks]), status
    except Exception as e:
        status = 500
        ERROR_COUNT.labels(method="GET", endpoint="/tasks", http_status=status).inc()
        return jsonify({"error": str(e)}), status
    finally:
        REQUEST_COUNT.labels(method="GET", endpoint="/tasks", http_status=status).inc()
        REQUEST_LATENCY.labels(method="GET", endpoint="/tasks").observe(
            time.time() - start_time
        )


@bp.route("/tasks", methods=["POST"])
def create_task():
    start_time = time.time()
    try:
        try:
            task_data = TaskCreate(**request.get_json())
        except ValidationError as e:
            status = 422
            ERROR_COUNT.labels(
                method="POST", endpoint="/tasks", http_status=status
            ).inc()
            return jsonify({"error": str(e)}), status
        task = TaskService.create_task(task_data)
        status = 201
        return jsonify(task.to_dict()), status
    except Exception as e:
        status = 500
        ERROR_COUNT.labels(method="POST", endpoint="/tasks", http_status=status).inc()
        return jsonify({"error": str(e)}), status
    finally:
        REQUEST_COUNT.labels(method="POST", endpoint="/tasks", http_status=status).inc()
        REQUEST_LATENCY.labels(method="POST", endpoint="/tasks").observe(
            time.time() - start_time
        )


@bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    start_time = time.time()
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            status = 404
            ERROR_COUNT.labels(
                method="GET", endpoint="/tasks/<id>", http_status=status
            ).inc()
            return jsonify({"error": f"Task {task_id} not found"}), status
        status = 200
        return jsonify(task.to_dict()), status
    except Exception as e:
        status = 500
        ERROR_COUNT.labels(
            method="GET", endpoint="/tasks/<id>", http_status=status
        ).inc()
        return jsonify({"error": str(e)}), status
    finally:
        REQUEST_COUNT.labels(
            method="GET", endpoint="/tasks/<id>", http_status=status
        ).inc()
        REQUEST_LATENCY.labels(method="GET", endpoint="/tasks/<id>").observe(
            time.time() - start_time
        )


@bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id: int):
    start_time = time.time()
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            status = 404
            ERROR_COUNT.labels(
                method="PUT", endpoint="/tasks/<id>", http_status=status
            ).inc()
            return jsonify({"error": f"Task {task_id} not found"}), status
        try:
            task_data = TaskUpdate(**request.get_json())
        except ValidationError as e:
            status = 422
            ERROR_COUNT.labels(
                method="PUT", endpoint="/tasks/<id>", http_status=status
            ).inc()
            return jsonify({"error": str(e)}), status
        updated_task = TaskService.update_task(task, task_data)
        status = 200
        return jsonify(updated_task.to_dict()), status
    except Exception as e:
        status = 500
        ERROR_COUNT.labels(
            method="PUT", endpoint="/tasks/<id>", http_status=status
        ).inc()
        return jsonify({"error": str(e)}), status
    finally:
        REQUEST_COUNT.labels(
            method="PUT", endpoint="/tasks/<id>", http_status=status
        ).inc()
        REQUEST_LATENCY.labels(method="PUT", endpoint="/tasks/<id>").observe(
            time.time() - start_time
        )


@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    start_time = time.time()
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            status = 404
            ERROR_COUNT.labels(
                method="DELETE", endpoint="/tasks/<id>", http_status=status
            ).inc()
            return jsonify({"error": f"Task {task_id} not found"}), status
        TaskService.delete_task(task)
        status = 204
        return "", status
    except Exception as e:
        status = 500
        ERROR_COUNT.labels(
            method="DELETE", endpoint="/tasks/<id>", http_status=status
        ).inc()
        return jsonify({"error": str(e)}), status
    finally:
        REQUEST_COUNT.labels(
            method="DELETE", endpoint="/tasks/<id>", http_status=status
        ).inc()
        REQUEST_LATENCY.labels(method="DELETE", endpoint="/tasks/<id>").observe(
            time.time() - start_time
        )


@bp.route("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
