from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_house():
    response = client.post("/api/houses", json={
        "name": "Smart Home",
        "address": "123 Main Street"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "House created successfully"

def test_duplicate_house():
    client.post("/api/houses", json={
        "name": "Smart Home",
        "address": "123 Main Street"
    })  # First creation

    response = client.post("/api/houses", json={
        "name": "Smart Home",
        "address": "456 Another Street"
    })  # Duplicate name
    assert response.status_code == 400
    assert response.json()["detail"] == "House with this name already exists"

def test_get_house():
    response = client.get("/api/houses/1")
    assert response.status_code == 200
    assert "name" in response.json()

def test_get_non_existent_house():
    response = client.get("/api/houses/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "House not found"
