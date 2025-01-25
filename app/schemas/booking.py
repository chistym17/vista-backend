from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

class BookingCreate(BaseModel):
    userId: str
    userEmail: str
    destination: str
    checkIn: str  # ISO format string
    checkOut: str  # ISO format string
    guests: int
    roomType: str
    contactInfo: ContactInfo
    bookingDate: str  # ISO format string
    status: str
    totalNights: int

class BookingResponse(BaseModel):
    id: str
    userId: str
    userEmail: str
    destination: str
    checkIn: str
    checkOut: str
    guests: int
    roomType: str
    contactInfo: ContactInfo
    bookingDate: str
    status: str
    totalNights: int
    totalAmount: float