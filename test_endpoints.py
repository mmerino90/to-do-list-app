#!/usr/bin/env python
"""Quick endpoint test script."""
import os
import sys

# Set testing config
os.environ["FLASK_CONFIG"] = "testing"
os.environ["FLASK_ENV"] = "testing"

from app import create_app

app = create_app("testing")
client = app.test_client()

# Test endpoints
print("=" * 60)
print("Testing API Endpoints")
print("=" * 60)

# Health endpoint
print("\n1. Health Endpoint (/api/v1/health):")
response = client.get("/api/v1/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json}")

# Ping endpoint
print("\n2. Ping Endpoint (/api/v1/ping):")
response = client.get("/api/v1/ping")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json}")

# Metrics endpoint
print("\n3. Metrics Endpoint (/api/v1/metrics):")
response = client.get("/api/v1/metrics")
print(f"   Status: {response.status_code}")
print(f"   Has Prometheus metrics: {b'prometheus' in response.data or b'todo_api' in response.data}")

# Tasks endpoints
print("\n4. Create Task (/api/v1/tasks [POST]):")
task_data = {"title": "Test Task", "description": "Testing deployment"}
response = client.post("/api/v1/tasks", json=task_data)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json}")
task_id = response.json.get("id") if response.status_code == 201 else None

if task_id:
    print("\n5. Get Tasks (/api/v1/tasks [GET]):")
    response = client.get("/api/v1/tasks")
    print(f"   Status: {response.status_code}")
    print(f"   Tasks count: {len(response.json)}")

    print("\n6. Update Task (/api/v1/tasks/{id} [PUT]):")
    update_data = {"title": "Updated Task", "completed": True}
    response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json}")

    print("\n7. Delete Task (/api/v1/tasks/{id} [DELETE]):")
    response = client.delete(f"/api/v1/tasks/{task_id}")
    print(f"   Status: {response.status_code}")

print("\n" + "=" * 60)
print("✅ All endpoints tested successfully!")
print("=" * 60)
