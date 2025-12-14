from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesSchemaAddData
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить все удобства")
@cache(expire=10)
async def get_facilities(db: DBDep):
    test_task.delay()
    return await db.facilities.get_all()


@router.post("", summary="Добавить удобства")
async def create_facility(db: DBDep, facility_data: FacilitiesSchemaAddData):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "Facility created", "facility": facility}
