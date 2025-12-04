from src.database import async_session_maker_null_pool
from src.schemas.hotels import HotelSchemaAddData
from src.utils.db_manager import DBManager


async def test_add_hotel():
    data = HotelSchemaAddData(title="Test Hotel", location="New York, Palm str. 23")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        result = await db.hotels.add(data)
        await db.commit()
        print(result)