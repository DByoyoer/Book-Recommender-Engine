from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Book
from schemas.book import BookSchema
from schemas.user import RatingSchema, ReadingListEntrySchema
from services.database import get_db_session
import random

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{user_id}")
async def get_user_info(user_id: int, db_session: AsyncSession = Depends(get_db_session)):
    pass


@router.get("/{user_id}/ratings", response_model=list[RatingSchema])
async def get_user_ratings(user_id: int, db_session: AsyncSession = Depends(get_db_session)):
    user = await db_session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.ratings


@router.get("/{user_id}/reading_list", response_model=list[ReadingListEntrySchema])
async def get_user_reading_list(user_id: int, db_session: AsyncSession = Depends(get_db_session)):
    user = await db_session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.reading_list


@router.get("/{user_id}/recs", response_model=list[BookSchema])
async def get_user_recs(user_id: int, db_session: AsyncSession = Depends(get_db_session)):
    # TODO: Actually utilize a recommendation engine :)
    rec_ids = random.choices(range(1, 10001), k=25)
    books = await db_session.scalars(
        select(Book).where(Book.id.in_(rec_ids))
    )
    return books.all()
