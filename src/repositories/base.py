from asyncpg import UniqueViolationError
from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exeptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, limit: int | None = None, offset: int = 0, **filter_by):
        query = (
            select(self.model).filter(*filter).filter_by(**filter_by).limit(limit).offset(offset)
        )
        result = await self.session.execute(query)
        model_orm = result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in model_orm]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model_orm = result.scalars().one_or_none()
        if model_orm is None:
            return None
        return self.mapper.map_to_domain_entity(model_orm)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model_orm = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model_orm)

    async def add(self, data: BaseModel):
        add_data_statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_data_statement)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else: raise ex
        model_orm = result.scalars().one()
        return self.mapper.map_to_domain_entity(model_orm)

    async def add_bulk(self, data: list[BaseModel]):
        if not data:
            return
        add_data_statement = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_statement)

    async def edit(self, update_data: BaseModel, exclude_unset: bool = False, **filter_by):
        try:
            await self.get_one(**filter_by)
        except NoResultFound:
            raise ObjectNotFoundException

        update_data_statement = (
            update(self.model)
            .filter_by(**filter_by)
            .values(update_data.model_dump(exclude_unset=exclude_unset))
        )
        return await self.session.execute(update_data_statement)

    async def delete(self, **filter_by):
        delete_data_statement = delete(self.model).filter_by(**filter_by)
        try:
            await self.get_one(**filter_by)
        except NoResultFound:
            raise ObjectNotFoundException
        return await self.session.execute(delete_data_statement)
