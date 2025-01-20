from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from .routes import booking  # Add this import

app = FastAPI(title="FastAPI MongoDB App")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.mongodb_uri)
    app.mongodb = app.mongodb_client.vista 

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI MongoDB API"}

# Add this line with the other router includes
app.include_router(booking.router, prefix="/api/bookings", tags=["bookings"]) 