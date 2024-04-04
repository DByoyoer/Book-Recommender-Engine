from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .book import book_author_association

# TODO: Consider migrating to a contributor table to have different roles (e.g Author, illustrator, editor, etc)
class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str]

    books: Mapped[List["Book"]] = relationship(secondary=book_author_association, back_populates="authors",lazy="selectin")

