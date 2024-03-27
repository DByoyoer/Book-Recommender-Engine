from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class ReadingList(Base):
    __tablename__ = "reading_list"
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    ranking: Mapped[int] = mapped_column(default=1)
    date_added: Mapped[datetime] = mapped_column(server_default=func.now())
    user: Mapped["User"] = relationship(back_populates="reading_list")