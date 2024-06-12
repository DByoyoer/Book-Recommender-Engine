from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

_naming_conventions = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=_naming_conventions)

from .author import Author
from .book import Book
from .genre import Genre
from .rating import Rating
from .reading_list import ReadingList
from .user import User
from .top_recs import TopRecommendations