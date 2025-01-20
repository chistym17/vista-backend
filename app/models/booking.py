from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RoomType(str, Enum):
    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"
    DELUXE = "deluxe"

class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class GuestInfo(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None

class BookingBase(BaseModel):
    room_type: RoomType
    check_in_date: datetime
    check_out_date: datetime
    number_of_guests: int = Field(gt=0)
    special_requests: Optional[str] = None
    room_number: Optional[str] = None
    total_price: float = Field(gt=0)

class BookingCreate(BookingBase):
    guest_info: GuestInfo

class BookingUpdate(BaseModel):
    room_type: Optional[RoomType] = None
    check_in_date: Optional[datetime] = None
    check_out_date: Optional[datetime] = None
    number_of_guests: Optional[int] = Field(None, gt=0)
    special_requests: Optional[str] = None
    room_number: Optional[str] = None
    total_price: Optional[float] = Field(None, gt=0)
    status: Optional[BookingStatus] = None

class BookingResponse(BookingBase):
    id: str
    guest_info: GuestInfo
    booking_reference: str
    status: BookingStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 