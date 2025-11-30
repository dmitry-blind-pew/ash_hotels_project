from src.mappers.rooms import RoomsMapper, RoomsMapperWithRelationships
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking

from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomsMapper


    async def get_rooms_filter_by_date(self, date_from: date, date_to: date, hotel_id):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to, hotel_id=hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        model_orm = result.unique().scalars().all()
        return [RoomsMapperWithRelationships.map_to_domain_entity(model) for model in model_orm]


    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model_orm = result.unique().scalars().one_or_none()
        if model_orm is None:
            return None
        return RoomsMapperWithRelationships.map_to_domain_entity(model_orm)

