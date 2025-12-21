from src.api.dependencies import UserIdDep
from src.exeptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundException
from src.schemas.bookings import BookingSchemaAdd, BookingSchemaAddRequest
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()


    async def get_bookings_me(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtered(user_id=user_id)


    async def create_booking(self, booking_data: BookingSchemaAdd, user_id: UserIdDep):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException as exc:
            raise RoomNotFoundException from exc
        hotel = await self.db.hotels.get_one(id=room.hotel_id)
        price = room.price
        booking_data_and_id = BookingSchemaAddRequest(user_id=user_id, price=price, **booking_data.model_dump())
        try:
            booking = await self.db.bookings.add_booking(data=booking_data_and_id, hotel_id=hotel.id)
        except AllRoomsAreBookedException as exc:
            raise AllRoomsAreBookedException from exc
        await self.db.commit()
        return booking