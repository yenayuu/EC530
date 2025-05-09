from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

router = APIRouter()

rooms_db: Dict[int, Dict] = {}
room_counter = 1

class RoomCreate(BaseModel):
    name: str = Field(..., min_length=2)
    floor: int = Field(..., ge=0)

@router.post("/houses/{house_id}/rooms")
def create_room(house_id: int, room: RoomCreate):
    global room_counter
    room_id = room_counter
    room_counter += 1
    rooms_db[room_id] = {
        "house_id": house_id,
        "name": room.name,
        "floor": room.floor
    }
    return {"message": "Room created", "room_id": room_id}

@router.get("/rooms/{room_id}")
def get_room(room_id: int):
    if room_id not in rooms_db:
        raise HTTPException(status_code=404, detail="Room not found")
    return rooms_db[room_id]

@router.get("/houses/{house_id}/rooms")
def get_rooms_by_house(house_id: int):
    house_rooms = [
        room for room in rooms_db.values()
        if room["house_id"] == house_id
    ]
    return house_rooms
