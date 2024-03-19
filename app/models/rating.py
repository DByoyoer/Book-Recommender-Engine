from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .user import User


class Rating(BaseModel):
    __tablename__ = "ratings"

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    rating_text: Mapped[str | None]
    rating: Mapped[int]
    date_created: Mapped[DateTime] = mapped_column(server_default=func.now())
    date_updated: Mapped[DateTime] = mapped_column(onupdate=func.now())

    user: Mapped[User] = relationship(back_populates="ratings")


