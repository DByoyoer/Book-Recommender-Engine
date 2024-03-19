from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .book import Book, book_genre_association


class Genre(BaseModel):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    books: Mapped[list[Book]] = relationship(secondary=book_genre_association, back_populates="genres")
