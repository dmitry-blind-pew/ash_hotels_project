from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database import BaseORM


class FacilitiesORM(BaseORM):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    rooms: Mapped[list["RoomsORM"]] = relationship(
        back_populates="facilities",
        secondary="facilities_and_rooms"
    )


class RoomsFacilitiesORM(BaseORM):
    __tablename__ = 'facilities_and_rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    facilities: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
    rooms: Mapped[int] = mapped_column(ForeignKey("rooms.id"))