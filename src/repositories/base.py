from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel


class BaseRepository:
    model = None
    schema: BaseModel = None


    def __init__(self, session):
        self.session = session


    async def get_filtered(
            self,
            *filter,
            limit: int | None = None,
            offset: int = 0,
            **filter_by
    ):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        model_orm = result.scalars().all()
        return [self.schema.model_validate(model, from_attributes=True) for model in model_orm]


    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model_orm = result.scalars().one_or_none()
        if model_orm is None:
            return None
        return self.schema.model_validate(model_orm, from_attributes=True)


    async def add(self, data: BaseModel):
        add_data_statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_statement)
        model_orm = result.scalars().one()
        return self.schema.model_validate(model_orm, from_attributes=True)


    async def add_bulk(self, data: list[BaseModel]):
        if not data:
            return
        add_data_statement = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_statement)


    async def edit(self, update_data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_data_statement = (update(self.model)
                                 .filter_by(**filter_by)
                                 .values(update_data.model_dump(exclude_unset=exclude_unset)))
        return await self.session.execute(update_data_statement)


    async def delete(self, **filter_by):
        delete_data_statement = delete(self.model).filter_by(**filter_by)
        return await self.session.execute(delete_data_statement)