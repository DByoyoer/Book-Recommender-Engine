from datetime import datetime

from pydantic import BaseModel
from .book import BookSchema


class RatingSchema(BaseModel):
    book_id: int
    score: int
    rating_text: str | None = ""
    date_created: datetime
    date_updated: datetime


class ReadingListEntrySchema(BaseModel):
    book_id: int
    ranking: int = 0
    date_added: datetime


class UserSchema(BaseModel):
    id: int
    username: str
    ratings: list[RatingSchema]
    reading_list: list[ReadingListEntrySchema]

class UserCreateSchema(BaseModel):
    username: str
