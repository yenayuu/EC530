from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Dict
import hashlib

router = APIRouter()

# In-memory storage for users (temporary, no database)
users_db: Dict[str, Dict] = {}

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/users/register")
def register_user(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    users_db[user.email] = {"name": user.name, "password": hashed_password}

    return {"message": "User registered successfully"}

@router.post("/users/login")
def login_user(user: UserLogin):
    if user.email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    if users_db[user.email]["password"] != hashed_password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": "Login successful", "user": {"name": users_db[user.email]["name"], "email": user.email}}
