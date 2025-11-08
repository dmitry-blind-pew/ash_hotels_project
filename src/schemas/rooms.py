from pydantic import BaseModel, Field


class RoomSchemaRequestData(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomSchemaAddData(RoomSchemaRequestData):
    hotel_id: int


class RoomSchema(RoomSchemaAddData):
    id: int


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomPatch(RoomPatchRequest):
    hotel_id: int | None = None