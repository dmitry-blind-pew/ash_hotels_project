from datetime import date

from src.schemas.hotels import HotelSchemaAddData, HotelPatch
from src.services.base import BaseService
from src.utils.exeptions import check_date_from_and_date_to


class HotelsService(BaseService):
    async def get_hotels(
        self,
        pagination,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):
        check_date_from_and_date_to(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filter_by_date(
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelSchemaAddData):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def put_hotel(self, hotel_id: int, hotel_data: HotelSchemaAddData):
        await self.db.hotels.edit(id=hotel_id, update_data=hotel_data)
        await self.db.commit()

    async def patch_hotel(self, hotel_id: int, hotel_data: HotelPatch):
        await self.db.hotels.edit(id=hotel_id, update_data=hotel_data, exclude_unset=True)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
