from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from ..schemas.booking import BookingCreate, BookingResponse
from bson import ObjectId
from pydantic import ValidationError

router = APIRouter()

@router.post("/", response_model=BookingResponse)
async def create_booking(request: Request, booking: BookingCreate = Body(...)):
    try:
        booking_dict = jsonable_encoder(booking)
        booking_dict["totalAmount"] = 299.0
        
        new_booking = await request.app.mongodb["bookings"].insert_one(booking_dict)
        
        if new_booking.inserted_id:
            created_booking = await request.app.mongodb["bookings"].find_one(
                {"_id": new_booking.inserted_id}
            )
            if created_booking:
                created_booking["id"] = str(created_booking["_id"])
                del created_booking["_id"]
                return created_booking
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create booking"
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error creating booking: {str(e)}")
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
            booking["id"] = str(booking["_id"])
            del booking["_id"]
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
            booking["id"] = str(booking["_id"])
            del booking["_id"]
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
                    updated_booking["id"] = str(updated_booking["_id"])
                    del updated_booking["_id"]
                    return updated_booking

        if (existing_booking := await request.app.mongodb["bookings"].find_one(
            {"_id": ObjectId(booking_id)}
        )) is not None:
            existing_booking["id"] = str(existing_booking["_id"])
            del existing_booking["_id"]
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
        booking = await request.app.mongodb["bookings"].find_one({"_id": ObjectId(booking_id)})
        if not booking:
            raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
            
        delete_result = await request.app.mongodb["bookings"].delete_one({"_id": ObjectId(booking_id)})
        
        if delete_result.deleted_count == 1:
            booking["id"] = str(booking["_id"])
            del booking["_id"]
            return {
                "status": "success",
                "message": f"Booking {booking_id} deleted",
                "deleted_booking": booking
            }
            
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 