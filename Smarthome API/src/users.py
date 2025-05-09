from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

router = APIRouter()

# In-memory database
users_db: Dict[int, Dict] = {}
user_counter = 1

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(..., pattern=r"[^@]+@[^@]+\.[^@]+")

@router.post("/users")
def create_user(user: UserCreate):
    global user_counter

    # Check for duplicate email
    if any(u["email"] == user.email for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = user_counter
    user_counter += 1
    users_db[user_id] = {"name": user.name, "email": user.email}

    return {"message": "User created", "user_id": user_id}

@router.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]
