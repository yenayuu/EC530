from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List

router = APIRouter()

# In-memory storage for rooms
rooms_db: Dict[int, Dict] = {}
room_counter = 1  # Simulates auto-incrementing IDs

# Allowed room types
VALID_ROOM_TYPES = {"bedroom", "kitchen", "living room", "bathroom"}

class RoomCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    room_type: str = Field(..., description="Must be one of: bedroom, kitchen, living room, bathroom")

@router.post("/houses/{house_id}/rooms")
def create_room(house_id: int, room: RoomCreate):
    global room_counter

    if room.room_type.lower() not in VALID_ROOM_TYPES:
        raise HTTPException(status_code=400, detail="Invalid room type")

    room_id = room_counter
    room_counter += 1
    rooms_db[room_id] = {"house_id": house_id, "name": room.name, "room_type": room.room_type}

    return {"message": "Room added successfully", "room_id": room_id}
