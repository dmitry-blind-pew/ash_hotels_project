from src.mappers.bookings import BookingsMapper
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingsMapper