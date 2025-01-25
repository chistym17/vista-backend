from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

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

    class Config:
        json_schema_extra = {
            "example": {
                "userId": "user123",
                "userEmail": "test@example.com",
                "destination": "Paris",
                "checkIn": "2024-03-20T14:00:00Z",
                "checkOut": "2024-03-25T11:00:00Z",
                "guests": 2,
                "roomType": "deluxe",
                "contactInfo": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+1234567890"
                },
                "bookingDate": "2024-03-15T10:30:00Z",
                "status": "pending",
                "totalNights": 5
            }
        }

class BookingResponse(BookingCreate):
    id: str = Field(alias="_id")
    totalAmount: float

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        allow_population_by_field_name = True 