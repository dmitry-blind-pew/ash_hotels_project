from pydantic import BaseModel, Field


class RoomSchemaRequestData(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = None


class RoomSchemaAddData(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomSchema(RoomSchemaAddData):
    id: int


class RoomSchemaPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None


class RoomSchemaPatch(RoomSchemaPatchRequest):
    hotel_id: int | None = None