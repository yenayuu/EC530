from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from main import app

client = TestClient(app)

def test_create_room():
    client.post("/api/houses", json={
        "name": "House for Room",
        "address": "456 Room Street"
    })

    response = client.post("/api/houses/1/rooms", json={
        "name": "Living Room",
        "floor": 1
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Room created"
    assert "room_id" in response.json()

def test_invalid_room_type():
    # This test is now irrelevant unless your schema restricts type manually
    # You can remove it OR expect 422 due to invalid schema field
    response = client.post("/api/houses/1/rooms", json={
        "name": "Invalid Room",
        "room_type": "garage"
    })
    assert response.status_code == 422  # schema mismatch

def test_get_rooms():
    client.post("/api/houses", json={
        "name": "House for List",
        "address": "List Street"
    })

    client.post("/api/houses/1/rooms", json={
        "name": "Room A",
        "floor": 1
    })

    response = client.get("/api/houses/1/rooms")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_non_existent_room():
    response = client.get("/api/rooms/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Room not found"
