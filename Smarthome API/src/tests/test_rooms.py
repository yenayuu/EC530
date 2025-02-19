from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_room():
    client.post("/api/houses", json={
        "name": "Smart Home",
        "address": "123 Main Street"
    })  # Ensure the house exists

    response = client.post("/api/houses/1/rooms", json={
        "name": "Living Room",
        "room_type": "living room"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Room added successfully"

def test_invalid_room_type():
    response = client.post("/api/houses/1/rooms", json={
        "name": "Invalid Room",
        "room_type": "garage"  # Invalid type
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid room type"

def test_get_rooms():
    response = client.get("/api/houses/1/rooms")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_non_existent_room():
    response = client.get("/api/rooms/999")
    assert response.status_code == 200
