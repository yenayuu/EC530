import sys
import os
from fastapi.testclient import TestClient

# Add src/ to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from main import app

client = TestClient(app)

def test_create_user_success():
    response = client.post("/api/users", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["message"] == "User created"

def test_create_user_duplicate_email():
    client.post("/api/users", json={"name": "Bob", "email": "bob@example.com"})
    response = client.post("/api/users", json={"name": "Bobby", "email": "bob@example.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_create_user_invalid_email():
    response = client.post("/api/users", json={"name": "Charlie", "email": "not-an-email"})
    assert response.status_code == 422  # FastAPI automatically validates schema

def test_get_user_success():
    post_response = client.post("/api/users", json={"name": "Diana", "email": "diana@example.com"})
    user_id = post_response.json()["user_id"]

    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 200
    user = get_response.json()
    assert user["name"] == "Diana"
    assert user["email"] == "diana@example.com"

def test_get_user_not_found():
    response = client.get("/api/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
