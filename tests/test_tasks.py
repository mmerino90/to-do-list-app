"""Test task API endpoints."""
import pytest
from app.models.task import Task

def test_create_task(client, db):
    """Test creating a task."""
    response = client.post("/api/v1/tasks", json={
        "title": "Test Task",
        "description": "Test Description"
    })
    assert response.status_code == 201
    assert response.json["title"] == "Test Task"
    assert response.json["description"] == "Test Description"

def test_get_tasks(client, db):
    """Test getting all tasks."""
    # Create a test task
    task = Task(title="Test Task")
    db.session.add(task)
    db.session.commit()
    
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Test Task"

def test_delete_task(client, db):
    """Test deleting a task."""
    # Create a test task
    task = Task(title="Test Task")
    db.session.add(task)
    db.session.commit()
    
    response = client.delete(f"/api/v1/tasks/{task.id}")
    assert response.status_code == 204
    
    # Verify task is deleted
    assert Task.query.get(task.id) is None

def test_update_task(client, db):
    """Test updating a task."""
    # Create a test task
    task = Task(title="Test Task")
    db.session.add(task)
    db.session.commit()
    
    response = client.put(f"/api/v1/tasks/{task.id}", json={
        "title": "Updated Task",
        "completed": True
    })
    assert response.status_code == 200
    assert response.json["title"] == "Updated Task"
    assert response.json["completed"] is True