from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.exeptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingSchemaAdd, BookingSchemaAddRequest
from src.api.dependencies import DBDep, UserIdDep


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получить все бронирования")
@cache(expire=10)
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получить мои бронирования")
@cache(expire=10)
async def get_bookings_me(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Создание бронирования")
async def create_booking(booking_data: BookingSchemaAdd, db: DBDep, user_id: UserIdDep):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    hotel = await db.hotels.get_one(id=room.hotel_id)
    price = room.price
    booking_data_and_id = BookingSchemaAddRequest(user_id=user_id, price=price, **booking_data.model_dump())
    try:
        booking = await db.bookings.add_booking(data=booking_data_and_id, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "Booking added", "data": booking}
