from pydantic import BaseModel, Field


class HotelSchemaAddData(BaseModel):
    title: str
    location: str


class HotelSchema(HotelSchemaAddData):
    id: int


class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
