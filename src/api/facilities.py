from fastapi import APIRouter
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesSchemaAddData

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("", summary="Получить все удобства")
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Добавить удобства")
async def create_facility(db: DBDep, facility_data: FacilitiesSchemaAddData):
    await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "Facility created"}