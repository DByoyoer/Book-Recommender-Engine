from __future__ import annotations
from pydantic import BaseModel


class Author(BaseModel):
    id: int
    name: str
    books: list[Book] = []

class Book(BaseModel):
    id: int
    title: str
    genres: list[str]
    authors: list[Author]
