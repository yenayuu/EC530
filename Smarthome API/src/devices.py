from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List

router = APIRouter()

# In-memory storage for devices
devices_db: Dict[int, Dict] = {}
device_counter = 1  # Simulates auto-incrementing IDs

# Allowed device types
VALID_DEVICE_TYPES = {"light", "thermostat", "fan", "camera"}

class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    device_type: str = Field(..., description="Must be one of: light, thermostat, fan, camera")
    status: str = Field(..., min_length=2, max_length=50)

@router.post("/rooms/{room_id}/devices")
def add_device(room_id: int, device: DeviceCreate):
    global device_counter

    if device.device_type.lower() not in VALID_DEVICE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid device type")

    device_id = device_counter
    device_counter += 1
    devices_db[device_id] = {"room_id": room_id, "name": device.name, "device_type": device.device_type, "status": device.status}

    return {"message": "Device added successfully", "device_id": device_id}
