from datetime import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    date_created: Mapped[datetime] = mapped_column(server_default = func.now())

    ratings: Mapped[List["Rating"]] = relationship(back_populates="user")
    reading_list: Mapped[List["ReadingList"]] = relationship(back_populates="user")