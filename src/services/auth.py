from src.config import settings
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import jwt

from src.exeptions import (
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
    IncorrectTokenException,
    EmailNotRegisteredException,
    IncorrectPasswordException,
)
from src.schemas.auth import UserAddDataSchema, UserHashedSchema
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def get_me(self, user_id: int):
        user = await self.db.users.get_one_or_none(id=user_id)
        return user

    async def login_user(self, user_data: UserAddDataSchema) -> str:
        user = await self.db.users.get_user_with_hashed_password(email=user_data.email)
        if user is None:
            raise EmailNotRegisteredException
        if not self.verify_password(user_data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def register_user(self, user_data: UserAddDataSchema):
        hashed_password = self.hash_password(user_data.password)
        hashed_user_data = UserHashedSchema(email=user_data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(hashed_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as exc:
            raise UserAlreadyExistsException from exc
