from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class Rating(Base):
    __tablename__ = "rating"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), primary_key=True)
    score: Mapped[float]
    rating_text: Mapped[str | None]
    date_created: Mapped[datetime] = mapped_column(server_default=func.now())
    date_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="ratings")


