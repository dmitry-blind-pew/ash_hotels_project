from pydantic import BaseModel, EmailStr


class UserAddDataSchema(BaseModel):
    email: EmailStr
    password: str


class UserHashedSchema(BaseModel):
    email: EmailStr
    hashed_password: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr
