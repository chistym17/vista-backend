from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from .routes import booking
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    mongodb_uri: str
    port: int = int(os.getenv("PORT", 8000))  # Add port setting

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

app = FastAPI(title="Vista Backend API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    try:
        app.mongodb_client = AsyncIOMotorClient(settings.mongodb_uri)
        app.mongodb = app.mongodb_client.vista
        print(f"Connected to MongoDB! Server running on port {settings.port}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    print("Disconnected from MongoDB!")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Vista Backend API",
        "status": "Connected to MongoDB"
    }

app.include_router(booking.router, prefix="/api/bookings", tags=["bookings"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True
    ) 