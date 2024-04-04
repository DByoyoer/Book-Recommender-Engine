from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.book import BookSchema
from schemas.user import RatingSchema, ReadingListEntrySchema
from services.database import get_db_session

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
    return user.ratings


@router.get("/{user_id}/reading_list", response_model=list[ReadingListEntrySchema])
async def get_user_reading_list(user_id: int, db_session: AsyncSession = Depends(get_db_session)):
    user = await db_session.get(User, user_id)
    return user.reading_list


@router.get("/{user_id}/recs", response_model=list[BookSchema])
async def get_user_recs(user_id: int):
    pass
