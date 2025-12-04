import json

import pytest
from httpx import AsyncClient
from sqlalchemy.dialects.mysql import insert

from src.config import settings
from src.database import BaseORM, engine_null_pool
from src.main import app
from src.models import *

@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)
        with (
            open("tests/test_data/mock_hotels.json", "r", encoding="utf-8") as hotels_file,
            open("tests/test_data/mock_rooms.json", "r", encoding="utf-8") as rooms_file
        ):
            hotels_data = json.load(hotels_file)
            rooms_data = json.load(rooms_file)
        await conn.execute(insert(HotelsORM).values(hotels_data))
        await conn.execute(insert(RoomsORM).values(rooms_data))
        await conn.commit()



@pytest.fixture(scope="session", autouse=True)
async def create_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={
                "email": "test@gmail.com",
                "password": "1234",
            }
        )
