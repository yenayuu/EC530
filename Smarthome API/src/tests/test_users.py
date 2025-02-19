from fastapi.testclient import TestClient
from src.main import app  # Importing the FastAPI app

client = TestClient(app)

def test_register_user():
    response = client.post("/api/users/register", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepass123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"

def test_duplicate_user():
    client.post("/api/users/register", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepass123"
    })  # First registration

    response = client.post("/api/users/register", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepass123"
    })  # Duplicate registration

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_invalid_email():
    response = client.post("/api/users/register", json={
        "name": "Jane Doe",
        "email": "invalid-email",
        "password": "securepass123"
    })
    assert response.status_code == 422  # Pydantic validation error

def test_login_success():
    client.post("/api/users/register", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepass123"
    })  # Ensure user exists

    response = client.post("/api/users/login", json={
        "email": "john.doe@example.com",
        "password": "securepass123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"

def test_login_wrong_password():
    response = client.post("/api/users/login", json={
        "email": "john.doe@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect password"
