from sqlalchemy import select
from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(self, location, title, limit, offset):
        query = select(self.model)
        if location is not None:
            query = query.filter(self.model.location.ilike(f"%{location}%"))
        if title is not None:
            query = query.filter(self.model.title.ilike(f"%{title}%"))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
