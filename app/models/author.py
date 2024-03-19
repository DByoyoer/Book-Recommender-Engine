from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .book import Book, book_author_association

# TODO: Consider migrating to a contributor table to have different roles (e.g Author, illustrator, editor, etc)
class Author(BaseModel):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primaryKey = True)
    name: Mapped[str]

    books: Mapped[List[Book]] = relationship(secondary=book_author_association, back_populates="authors")

