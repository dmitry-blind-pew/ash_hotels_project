from sqlalchemy import select
from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemas.auth import UserSchema, UserLoginHashedSchema
from pydantic import EmailStr


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = UserSchema

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model_orm = result.scalars().one()
        return UserLoginHashedSchema.model_validate(model_orm, from_attributes=True)


