from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.exeptions import AllRoomsAreBookedException, RoomNotFoundException, \
    RoomNotFoundHTTPException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingSchemaAdd
from src.api.dependencies import DBDep, UserIdDep
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получить все бронирования")
@cache(expire=10)
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_bookings()


@router.get("/me", summary="Получить мои бронирования")
@cache(expire=10)
async def get_bookings_me(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_bookings_me(user_id=user_id)


@router.post("", summary="Создание бронирования")
async def create_booking(booking_data: BookingSchemaAdd, db: DBDep, user_id: UserIdDep):
    try:
        booking = await BookingService(db).create_booking(booking_data=booking_data, user_id=user_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "Booking added", "data": booking}
