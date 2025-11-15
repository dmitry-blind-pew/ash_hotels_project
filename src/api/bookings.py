from fastapi import APIRouter

from src.schemas.bookings import BookingSchemaAdd, BookingSchemaAddRequest
from src.api.dependencies import DBDep, UserIdDep


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", description="Получить все бронирования")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", description="Получить мои бронирования")
async def get_bookings_me(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", description="Создание бронирования")
async def create_booking(booking_data: BookingSchemaAdd, db: DBDep, user_id: UserIdDep):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    price = room.price
    booking_data_and_id = BookingSchemaAddRequest(user_id=user_id, price=price, **booking_data.model_dump())
    booking = await db.bookings.add(booking_data_and_id)
    await db.commit()
    return {"status": "Booking added", "data": booking}

