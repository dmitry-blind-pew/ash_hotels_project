from pydantic import BaseModel, EmailStr, ConfigDict


class UserAddDataSchema(BaseModel):
    email: EmailStr
    password: str


class UserHashedSchema(BaseModel):
    email: EmailStr
    hashed_password: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserLoginHashedSchema(UserSchema):
    hashed_password: str
