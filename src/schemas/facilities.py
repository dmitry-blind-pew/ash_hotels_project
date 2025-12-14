from pydantic import BaseModel


class FacilitiesSchemaAddData(BaseModel):
    title: str


class FacilitiesSchema(FacilitiesSchemaAddData):
    id: int


class RoomsFacilitiesAddSchema(BaseModel):
    rooms: int
    facilities: int


class RoomsFacilitiesSchema(RoomsFacilitiesAddSchema):
    id: int
