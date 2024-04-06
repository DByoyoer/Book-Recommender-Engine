from __future__ import annotations
from pydantic import BaseModel, Field


class GenreSchema(BaseModel):
    id: int
    name: str


class AuthorBase(BaseModel):
    id: int
    name: str


class AuthorFullSchema(AuthorBase):
    books: list[BookBase]


class BookBase(BaseModel):
    id: int
    title: str
    cover_url: str
    genres: list[GenreSchema]


class BookSchema(BookBase):
    authors: list[AuthorBase]


class BookDetailedSchema(BookBase):
    authors: list[AuthorBase]
    description: str
    isbn: str | None = ""
    isbn13: str | None = ""
    lang_code: str
    pages: int
    original_publication_year: int | None
