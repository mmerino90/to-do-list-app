import pytest
from app import create_app

def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_metrics_endpoint(client):
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    assert b"python_gc_objects_collected_total" in response.data

def test_not_found_error(client):
    response = client.get("/api/v1/tasks/99999")
    assert response.status_code == 404
    assert "not found" in response.json["error"].lower()

def test_unprocessable_entity(client):
    # Missing required title
    response = client.post("/api/v1/tasks", json={"description": "desc only"})
    assert response.status_code == 422
    assert "error" in response.json

def test_internal_server_error(monkeypatch, client):
    # Simulate an exception in the service layer
    monkeypatch.setattr("app.services.task_service.TaskService.get_all_tasks", lambda: 1/0)
    response = client.get("/api/v1/tasks")
    assert response.status_code == 500
    assert "error" in response.json
