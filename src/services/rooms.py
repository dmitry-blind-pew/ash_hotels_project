from datetime import date

from src.exeptions import ObjectAlreadyExistsException, ObjectNotFoundException, RoomNotFoundException, \
    HotelNotFoundException
from src.schemas.facilities import RoomsFacilitiesAddSchema
from src.schemas.rooms import RoomSchemaRequestData, RoomSchemaAddData, RoomSchemaPatchRequest, RoomSchemaPatch
from src.services.base import BaseService
from src.utils.exeptions import check_date_from_and_date_to


class RoomService(BaseService):
    async def get_rooms(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        check_date_from_and_date_to(date_from, date_to)
        return await self.db.rooms.get_rooms_filter_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


    async def get_room(self, hotel_id: int, room_id: int):
        try:
            return await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException as exc:
            raise RoomNotFoundException from exc


    async def create_room(self, hotel_id: int, room_data: RoomSchemaRequestData):
        room_data_and_id = RoomSchemaAddData(hotel_id=hotel_id, **room_data.model_dump())
        try:
            room = await self.db.rooms.add(room_data_and_id)
        except ObjectAlreadyExistsException as exc:
            raise HotelNotFoundException from exc

        rooms_facilities_data = [
            RoomsFacilitiesAddSchema(rooms=room.id, facilities=facility_id) for facility_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room


    async def put_room(self, hotel_id: int, room_id: int, room_data: RoomSchemaRequestData):
        room_data_without_facilities = room_data.model_dump(exclude={"facilities_ids"})
        room_data_and_id = RoomSchemaAddData(hotel_id=hotel_id, **room_data_without_facilities)
        try:
            await self.db.rooms.edit(id=room_id, update_data=room_data_and_id)
        except ObjectNotFoundException as exc:
            raise RoomNotFoundException from exc
        await self.db.rooms_facilities.update_facilities(room_id=room_id, new_facilities_ids=room_data.facilities_ids)
        await self.db.commit()


    async def patch_room(self, hotel_id: int, room_id: int, room_data: RoomSchemaPatchRequest):
        try:
            await self.db.rooms_facilities.update_facilities(room_id=room_id, new_facilities_ids=room_data.facilities_ids)
        except ObjectNotFoundException as exc:
            raise RoomNotFoundException from exc

        room_data_dict = room_data.model_dump(exclude_unset=True, exclude={"facilities_ids"})
        room_data_and_id = RoomSchemaPatch(hotel_id=hotel_id, **room_data_dict)
        try:
            await self.db.rooms.edit(id=room_id, hotel_id=hotel_id, update_data=room_data_and_id, exclude_unset=True)
        except ObjectNotFoundException as exc:
            raise RoomNotFoundException from exc

        await self.db.commit()


    async def delete_room(self, hotel_id: int, room_id: int):
        try:
            await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException as exc:
            raise RoomNotFoundException from exc
        await self.db.commit()
