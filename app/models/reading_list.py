from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .user import User


class ReadingList(BaseModel):
    __tablename__ = "reading_list"
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    ranking: Mapped[int]
    date_added: Mapped[DateTime] = mapped_column(server_default=func.now())
    user: Mapped[User] = relationship(back_populates="reading_list")