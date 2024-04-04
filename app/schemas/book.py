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
