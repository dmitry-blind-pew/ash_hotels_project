from pydantic import BaseModel


class HotelSchemaAddData(BaseModel):
    title: str
    location: str


class HotelSchema(HotelSchemaAddData):
    id: int


class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None
