from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesSchemaAddData
from src.services.facilities import FacilitiesService


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить все удобства")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilitiesService(db).get_facilities()


@router.post("", summary="Добавить удобства")
async def create_facility(db: DBDep, facility_data: FacilitiesSchemaAddData):
    facility = await FacilitiesService(db).create_facility(facility_data)
    return {"status": "Facility created", "facility": facility}
