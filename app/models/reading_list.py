from datetime import datetime
from sqlalchemy import ForeignKey, func, text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class ReadingList(Base):
    __tablename__ = "reading_list"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), primary_key=True)
    ranking: Mapped[int] = mapped_column(server_default=text("0"))
    date_added: Mapped[datetime] = mapped_column(server_default=func.now())
    user: Mapped["User"] = relationship(back_populates="reading_list")
