from fastapi import APIRouter, HTTPException, Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.booking import BookingCreate, BookingResponse, BookingUpdate, BookingStatus
from datetime import datetime
from bson import ObjectId
import uuid

router = APIRouter()

async def get_database(request: Request) -> AsyncIOMotorDatabase:
    return request.app.mongodb

@router.post("/", response_model=BookingResponse)
async def create_booking(booking: BookingCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    booking_dict = booking.model_dump()
    booking_dict.update({
        "booking_reference": str(uuid.uuid4().hex[:8].upper()),
        "status": BookingStatus.PENDING,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    result = await db.bookings.insert_one(booking_dict)
    
    created_booking = await db.bookings.find_one({"_id": result.inserted_id})
    created_booking["id"] = str(created_booking["_id"])
    
    return BookingResponse(**created_booking)

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking ID")
        
    booking = await db.bookings.find_one({"_id": ObjectId(booking_id)})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking["id"] = str(booking["_id"])
    return BookingResponse(**booking)

@router.get("/", response_model=list[BookingResponse])
async def get_bookings(
    skip: int = 0, 
    limit: int = 10,
    status: BookingStatus = None,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    query = {}
    if status:
        query["status"] = status
        
    bookings = []
    cursor = db.bookings.find(query).skip(skip).limit(limit)
    async for booking in cursor:
        booking["id"] = str(booking["_id"])
        bookings.append(BookingResponse(**booking))
    return bookings

@router.patch("/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: str, 
    booking_update: BookingUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking ID")
        
    update_data = booking_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    updated_booking = await db.bookings.find_one({"_id": ObjectId(booking_id)})
    updated_booking["id"] = str(updated_booking["_id"])
    return BookingResponse(**updated_booking)

@router.delete("/{booking_id}")
async def delete_booking(booking_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking ID")
        
    result = await db.bookings.delete_one({"_id": ObjectId(booking_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    return {"message": "Booking deleted successfully"} 