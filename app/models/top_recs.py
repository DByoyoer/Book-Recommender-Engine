from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class TopRecommendations(Base):
    __tablename__ = "top_recs"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), primary_key=True)
    prediction: Mapped[float] = mapped_column(index=True)
    date_predicted: Mapped[datetime] = mapped_column(server_default=func.now())

    def __str__(self):
        return f"(user_id={self.user_id}, book_id={self.book_id}, prediction={self.prediction}, date_predicted={self.date_predicted})"
    def __repr__(self):
        return str(self)