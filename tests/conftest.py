import json
from unittest import mock

from src.api.dependencies import get_db

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import AsyncClient

from src.config import settings
from src.database import BaseORM, engine, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelSchemaAddData
from src.schemas.rooms import RoomSchemaAddData
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_manager_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db_manager() -> DBManager:
    async for db in get_db_manager_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_manager_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)

    with (
        open("tests/test_data/mock_hotels.json", "r", encoding="utf-8") as hotels_file,
        open("tests/test_data/mock_rooms.json", "r", encoding="utf-8") as rooms_file
    ):
        hotels_data = json.load(hotels_file)
        rooms_data = json.load(rooms_file)
    hotels_schemas = [HotelSchemaAddData.model_validate(hotel) for hotel in hotels_data]
    rooms_schemas = [RoomSchemaAddData.model_validate(room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels_schemas)
        await db.rooms.add_bulk(rooms_schemas)
        await db.commit()


@pytest.fixture(scope="session")
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as aclient:
        yield aclient


@pytest.fixture(scope="session", autouse=True)
async def create_user(async_client, setup_database):
    await async_client.post(
        "/auth/register",
        json={
            "email": "test@gmail.com",
            "password": "1234",
        }
    )


@pytest.fixture(scope="session")
async def auth_async_client(create_user, async_client):
    await async_client.post(
        "/auth/login",
        json={
            "email": "test@gmail.com",
            "password": "1234",
        }
    )
    assert async_client.cookies["access_token"]
    yield async_client
