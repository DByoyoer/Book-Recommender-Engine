from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .book import book_genre_association


class Genre(Base):
    __tablename__ = "genre"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    books: Mapped[list["Book"]] = relationship(secondary=book_genre_association, back_populates="genres")
