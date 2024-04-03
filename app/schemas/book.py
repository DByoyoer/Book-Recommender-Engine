from __future__ import annotations
from pydantic import BaseModel


class AuthorSchema(BaseModel):
    id: int
    name: str

class GenreSchema(BaseModel):
    id: int
    name: str

class BookSchema(BaseModel):
    id: int
    title: str
    genres: list[GenreSchema]
    authors: list[AuthorSchema]
