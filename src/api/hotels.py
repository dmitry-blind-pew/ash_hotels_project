from fastapi import Query, APIRouter
from datetime import date
from fastapi_cache.decorator import cache

from src.schemas.hotels import HotelSchemaAddData, HotelPatch
from src.api.dependencies import PaginationDep, DBDep


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Информация об отелях")
# @cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
    date_from: date = Query(example="2025-11-11"),
    date_to: date = Query(example="2025-11-12")
):
    per_page = pagination.per_page or 5
    return await (db.hotels.get_filter_by_date(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    ))


@router.get("{hotel_id}", summary="Поиск отеля по ID")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", summary="Добавление отелей")
async def create_hotel(hotel_data: HotelSchemaAddData, db: DBDep):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "Hotel created", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Обновление всех данных отеля",
    description="Необходимо вносить абсолютно все параметры для изменения"
)
async def put_hotel(hotel_id: int, hotel_data: HotelSchemaAddData, db: DBDep):
    await db.hotels.edit(id=hotel_id, update_data=hotel_data)
    await db.commit()
    return {"status": "Hotel updated"}


@router.patch("/{hotel_id}", summary="Обновление отдельных параметров отеля")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(id=hotel_id, update_data=hotel_data, exclude_unset=True)
    await db.commit()
    return {"status": "Hotel updated"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"Hotel deleted"}
