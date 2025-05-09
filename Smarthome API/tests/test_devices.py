from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from main import app


client = TestClient(app)

def test_add_device():
    client.post("/api/houses", json={
        "name": "Smart Home",
        "address": "123 Main Street"
    })  # Ensure house exists

    client.post("/api/houses/1/rooms", json={
        "name": "Living Room",
        "room_type": "living room"
    })  # Ensure room exists

    response = client.post("/api/rooms/1/devices", json={
        "name": "Smart Light",
        "device_type": "light",
        "status": "off"
    })
    assert response.status_code == 200
