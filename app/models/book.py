from typing import Optional, List

from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .author import Author
from .book_genre import Genre

book_author_association = Table("book_authors", BaseModel.metadata,
                                Column("book_id", ForeignKey("books.id"), primary_key=True),
                                Column("author_id", ForeignKey("authors.id"), primary_key=True)
                                )

book_genre_association = Table("book_genre", BaseModel.metadata,
                               Column("book_id", ForeignKey("books.id"), primary_key=True),
                               Column("genre_id", ForeignKey("genres.id"), primary_key=True)
                               )




# noinspection SpellCheckingInspection
class Book(BaseModel):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[Optional[str]] = mapped_column(String(12))
    lang_code = Mapped[Optional[str]] = mapped_column(String(10))
    title: Mapped[str]
    description: Mapped[Optional[str]]
    cover_url: Mapped[Optional[str]]
    original_publication_year: Mapped[Optional[int]]
    authors: Mapped[List[Author]] = relationship(secondary=book_author_association, back_populates="books")
    genres: Mapped[List[Genre]] = relationship(secondary=book_genre_association, back_populates="books")
