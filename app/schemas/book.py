from __future__ import annotations
from pydantic import BaseModel


class AuthorSchema(BaseModel):
    id: int
    name: str
    books: list[BookSchema] = []

class BookSchema(BaseModel):
    id: int
    title: str
    genres: list[str]
    authors: list[AuthorSchema]
