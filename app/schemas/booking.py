from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class ContactInfo(BaseModel):
    name: str
    email: EmailStr
    phone: str

class BookingCreate(BaseModel):
    userId: str
    userEmail: EmailStr
    destination: str
    checkIn: datetime
    checkOut: datetime
    guests: int
    roomType: str
    contactInfo: ContactInfo
    bookingDate: datetime
    status: str
    totalNights: int

class BookingResponse(BookingCreate):
    id: str
    totalAmount: float

    class Config:
        from_attributes = True 