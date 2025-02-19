from fastapi import FastAPI
from src.users import router as users_router
from src.houses import router as houses_router
from src.rooms import router as rooms_router
from src.devices import router as devices_router

app = FastAPI(title="Smart Home API", description="API for managing users, houses, rooms, and devices.")

# Registering API routers
app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(houses_router, prefix="/api", tags=["Houses"])
app.include_router(rooms_router, prefix="/api", tags=["Rooms"])
app.include_router(devices_router, prefix="/api", tags=["Devices"])

@app.get("/")
def home():
    return {"message": "Welcome to the Smart Home API"}
