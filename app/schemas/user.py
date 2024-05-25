from pydantic import BaseModel
from .custom_serializers import DateTimeWithoutTZ


class RatingSchema(BaseModel):
    book_id: int
    score: float
    rating_text: str | None = ""
    date_created: DateTimeWithoutTZ|None
    date_updated: DateTimeWithoutTZ|None




class ReadingListEntrySchema(BaseModel):
    book_id: int
    ranking: int = 0
    date_added: DateTimeWithoutTZ


class UserSchema(BaseModel):
    id: int
    username: str
    ratings: list[RatingSchema]
    reading_list: list[ReadingListEntrySchema]

class UserCreateSchema(BaseModel):
    username: str
