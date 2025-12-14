from time import sleep
import asyncio

from src.database import async_session_maker_null_pool
from src.tasks.celery_application import celery_app
from src.utils.db_manager import DBManager


@celery_app.task
def test_task():
    sleep(3)
    print("test_task")


async def send_email_for_today_checkin_helper():
    print("поиск начался")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings_for_send = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings_for_send}")


@celery_app.task(name="email_for_today_checkin")
def send_email_for_today_checkin():
    asyncio.run(send_email_for_today_checkin_helper())
