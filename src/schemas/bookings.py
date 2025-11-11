from pydantic import BaseModel
from datetime import date


class BookingSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class BookingSchemaAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingSchemaAddRequest(BookingSchemaAdd):
    user_id: int
    price: int