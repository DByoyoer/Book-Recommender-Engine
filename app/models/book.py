from typing import List

from sqlalchemy import ForeignKey, String, Table, Column, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

# TODO: Convert this to association object to include an 'order' field to indicate correct order to list the authors
book_author_association = Table(
    "book_author", Base.metadata,
    Column("book_id", ForeignKey("book.id"), primary_key=True),
    Column("author_id", ForeignKey("author.id"), primary_key=True)
)

book_genre_association = Table(
    "book_genre", Base.metadata,
    Column("book_id", ForeignKey("book.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True)
)


# noinspection SpellCheckingInspection
class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    goodreads_id: Mapped[int]
    title: Mapped[str]
    description: Mapped[str | None]
    isbn: Mapped[str | None] = mapped_column(String(12))
    isbn13: Mapped[str | None] = mapped_column(String(15))
    lang_code: Mapped[str | None] = mapped_column(String(10))
    pages: Mapped[int | None]
    cover_url: Mapped[str | None]
    original_publication_year: Mapped[int | None]
    authors: Mapped[List["Author"]] = relationship(
        secondary=book_author_association, back_populates="books", lazy="selectin"
    )
    genres: Mapped[List["Genre"]] = relationship(
        secondary=book_genre_association, back_populates="books", lazy="selectin"
    )

    @classmethod
    async def get_by_id(cls, db_session: AsyncSession, book_id: int):
        book = await db_session.get(cls, book_id)
        return book

    @classmethod
    async def get_by_isbn(cls, db_session: AsyncSession, isbn: str):
        book = (await db_session.scalars(select(cls).where(cls.isbn == isbn))).first()
        return book

    @classmethod
    async def get_list(cls, db_session: AsyncSession, book_ids: list[int]):
        result = await db_session.scalars(select(cls).where(cls.id.in_(list)))
        return result.all()

#TODO: Create fts tables for book title and columns to speed up search