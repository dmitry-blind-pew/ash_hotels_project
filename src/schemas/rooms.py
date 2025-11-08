from pydantic import BaseModel, Field


class RoomSchemaAddData(BaseModel):
    title: str
    hotel_id: int
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomSchema(RoomSchemaAddData):
    id: int


class RoomPatch(BaseModel):
    title: str | None = Field(None)
    hotel_id: int | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)