from typing import Optional, List

from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

# TODO: Convert this to association object to include an 'order' field to indicate correct order to list the authors
book_author_association = Table("book_authors", Base.metadata,
                                Column("book_id", ForeignKey("book.id"), primary_key=True),
                                Column("author_id", ForeignKey("author.id"), primary_key=True)
                                )

book_genre_association = Table("book_genre", Base.metadata,
                               Column("book_id", ForeignKey("book.id"), primary_key=True),
                               Column("genre_id", ForeignKey("genre.id"), primary_key=True)
                               )


# noinspection SpellCheckingInspection
class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[Optional[str]] = mapped_column(String(12))
    lang_code: Mapped[str | None] = mapped_column(String(10))
    pages: Mapped[int | None]
    title: Mapped[str]
    description: Mapped[str | None]
    cover_url: Mapped[str | None]
    original_publication_year: Mapped[int | None]
    authors: Mapped[List["Author"]] = relationship(secondary=book_author_association, back_populates="books")
    genres: Mapped[List["Genre"]] = relationship(secondary=book_genre_association, back_populates="books")
