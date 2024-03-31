from datetime import datetime

from pydantic import BaseModel
from book import Book

class Rating(BaseModel):
    book: Book
    rating: int
    rating_text: str
    date_created: datetime
    date_updated: datetime

class ReadingListEntry:
    book: Book
    ranking: int = 0
    date_added: datetime

class User(BaseModel):
    id: int
    username: str
    ratings: list[Rating]
    reading_list: list[ReadingListEntry]
