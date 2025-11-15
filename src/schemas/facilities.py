from pydantic import BaseModel


class FacilitiesSchemaAddData(BaseModel):
    title: str


class FacilitiesSchema(FacilitiesSchemaAddData):
    id: int