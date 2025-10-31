from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_statement)
        return result.scalars().one()

    async def delete(self, id):
        delete_data_statement = delete(self.model).where(self.model.id == id)
        return await self.session.execute(delete_data_statement)

    async def edit(self, id, update_data, exclude_unset: bool = False):
        update_data_statement = (update(self.model)
                                 .where(self.model.id == id)
                                 .values(update_data.model_dump(exclude_unset=exclude_unset)))
        return await self.session.execute(update_data_statement)