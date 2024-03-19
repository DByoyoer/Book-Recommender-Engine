from typing import List

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .rating import Rating
from .reading_list import ReadingList


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    date_created: Mapped[DateTime] = mapped_column(server_default = func.now())

    ratings: Mapped[List[Rating]] = relationship(back_populates="user")
    reading_list: Mapped[List[ReadingList]] = relationship(back_populates="user")