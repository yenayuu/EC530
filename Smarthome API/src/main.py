from users import router as users_router
from houses import router as houses_router
from rooms import router as rooms_router
from devices import router as devices_router

from fastapi import FastAPI

app = FastAPI(title="Smart Home API")

app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(houses_router, prefix="/api", tags=["Houses"])
app.include_router(rooms_router, prefix="/api", tags=["Rooms"])
app.include_router(devices_router, prefix="/api", tags=["Devices"])

@app.get("/")
def home():
    return {"message": "Welcome to the Smart Home API"}
