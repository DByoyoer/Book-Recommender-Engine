from datetime import datetime

from pydantic import BaseModel
from book import BookSchema

class RatingSchema(BaseModel):
    book: BookSchema
    rating: int
    rating_text: str
    date_created: datetime
    date_updated: datetime

class ReadingListEntrySchema:
    book: BookSchema
    ranking: int = 0
    date_added: datetime

class UserSchema(BaseModel):
    id: int
    username: str
    ratings: list[RatingSchema]
    reading_list: list[ReadingListEntrySchema]
