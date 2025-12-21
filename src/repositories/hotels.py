from src.mappers.hotels import HotelsMapper
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking


from sqlalchemy import select
from datetime import date


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelsMapper

    async def get_filter_by_date(
        self,
        date_from: date,
        date_to: date,
        location: str | None = None,
        title: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = select(RoomsORM.hotel_id).select_from(RoomsORM).filter(RoomsORM.id.in_(rooms_ids_to_get))

        filters = [self.model.id.in_(hotels_ids_to_get)]
        if location is not None:
            filters.append(self.model.location.ilike(f"%{location}%"))
        if title is not None:
            filters.append(self.model.title.ilike(f"%{title}%"))

        return await self.get_filtered(*filters, limit=limit, offset=offset)
