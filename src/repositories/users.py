from sqlalchemy import select

from src.mappers.users import UsersMapperHashed, UsersMapper
from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from pydantic import EmailStr


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UsersMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model_orm = result.scalars().one()
        return UsersMapperHashed.map_to_domain_entity(model_orm)


