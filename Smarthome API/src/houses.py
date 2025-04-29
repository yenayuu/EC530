from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List

router = APIRouter()

# In-memory storage for houses
houses_db: Dict[int, Dict] = {}
house_counter = 1  # Simulates auto-incrementing IDs

class HouseCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    address: str = Field(..., min_length=5, max_length=200)

@router.post("/houses")
def create_house(house: HouseCreate):
    global house_counter

    # Check for duplicate names
    if any(h["name"] == house.name for h in houses_db.values()):
        raise HTTPException(status_code=400, detail="House with this name already exists")

    house_id = house_counter
    house_counter += 1
    houses_db[house_id] = {"name": house.name, "address": house.address}

    return {"message": "House created successfully", "house_id": house_id}

@router.get("/houses/{house_id}")
def get_house(house_id: int):
    if house_id not in houses_db:
        raise HTTPException(status_code=404, detail="House not found")
    return houses_db[house_id]
