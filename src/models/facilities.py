from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from src.database import BaseORM


class FacilitiesORM(BaseORM):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]


class FacilitiesAndRoomsORM(BaseORM):
    __tablename__ = 'facilities_and_rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    facilities: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
    rooms: Mapped[int] = mapped_column(ForeignKey("rooms.id"))