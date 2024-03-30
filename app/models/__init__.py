from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

from .author import Author
from .book import Book
from .genre import Genre
from .rating import Rating
from .reading_list import ReadingList
from .user import User