from src.schemas.hotels import HotelSchemaAddData


async def test_add_hotel(db_manager):
    data = HotelSchemaAddData(title="Test Hotel", location="New York, Palm str. 23")
    result = await db_manager.hotels.add(data)
    await db_manager.commit()
    print(result)