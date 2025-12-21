import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database import BaseORM

if typing.TYPE_CHECKING:
    from src.models import FacilitiesORM


class RoomsORM(BaseORM):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    facilities: Mapped[list["FacilitiesORM"]] = relationship(back_populates="rooms", secondary="facilities_and_rooms")
