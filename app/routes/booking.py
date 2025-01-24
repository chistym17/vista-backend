from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from ..schemas.booking import BookingCreate, BookingResponse
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=BookingResponse)
async def create_booking(request: Request, booking: BookingCreate = Body(...)):
    try:
        booking = jsonable_encoder(booking)
        booking["totalAmount"] = 299.0
        
        new_booking = await request.app.mongodb["bookings"].insert_one(booking)
        created_booking = await request.app.mongodb["bookings"].find_one(
            {"_id": new_booking.inserted_id}
        )
        
        return created_booking
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/user/{user_id}", response_model=List[BookingResponse])
async def get_user_bookings(request: Request, user_id: str):
    bookings = []
    try:
        cursor = request.app.mongodb["bookings"].find({"userId": user_id})
        async for booking in cursor:
            bookings.append(booking)
        return bookings
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(request: Request, booking_id: str):
    try:
        if (booking := await request.app.mongodb["bookings"].find_one({"_id": ObjectId(booking_id)})) is not None:
            return booking
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(request: Request, booking_id: str, booking: BookingCreate = Body(...)):
    try:
        booking = {k: v for k, v in booking.dict().items() if v is not None}
        
        if len(booking) >= 1:
            update_result = await request.app.mongodb["bookings"].update_one(
                {"_id": ObjectId(booking_id)}, {"$set": booking}
            )
            
            if update_result.modified_count == 1:
                if (updated_booking := await request.app.mongodb["bookings"].find_one(
                    {"_id": ObjectId(booking_id)}
                )) is not None:
                    return updated_booking

        if (existing_booking := await request.app.mongodb["bookings"].find_one(
            {"_id": ObjectId(booking_id)}
        )) is not None:
            return existing_booking

        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{booking_id}")
async def delete_booking(request: Request, booking_id: str):
    try:
        delete_result = await request.app.mongodb["bookings"].delete_one({"_id": ObjectId(booking_id)})
        
        if delete_result.deleted_count == 1:
            return {"status": "success", "message": f"Booking {booking_id} deleted"}
            
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 