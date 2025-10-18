from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    status: str


class HotelPatch(BaseModel):
    title: str | None = Field(None)
    status: str | None = Field(None)