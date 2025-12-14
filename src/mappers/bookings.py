from src.mappers.base import DataMapper
from src.models.bookings import BookingsORM
from src.schemas.bookings import BookingSchema


class BookingsMapper(DataMapper):
    db_model = BookingsORM
    schema = BookingSchema
