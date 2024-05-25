from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, delete, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Book, ReadingList, Rating
from schemas.book import BookSchema
from schemas.user import RatingSchema, ReadingListEntrySchema, UserCreateSchema
from services.database import get_db_session
import random

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateSchema, db_session: AsyncSession = Depends(get_db_session)):
    new_user = User(username=user.username)
    db_session.add(new_user)
    await db_session.commit()
    return {"id": new_user.id, "username": new_user.username}


@router.get("/{user_id}")
async def get_user_info(user_id: int, db_session: AsyncSession = Depends(get_db_session)):
    pass


@router.get("/{user_id}/ratings", response_model=list[RatingSchema])
async def get_user_ratings(user_id: int, db_session: AsyncSession = Depends(get_db_session)):
    user = await db_session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.ratings


@router.post("/{user_id}/ratings", status_code=status.HTTP_201_CREATED)
async def add_rating(user_id: int, rating: RatingSchema, db_session: AsyncSession = Depends(get_db_session)):
    user = await db_session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    rating = Rating(user_id=user_id, **rating.model_dump())
    user.ratings.append(rating)
    await db_session.commit()
    return {"message": "created"}


@router.put("/{user_id}/ratings/{book_id}")
async def update_rating(
        user_id: int, book_id: int, rating: RatingSchema, db_session: AsyncSession = Depends(get_db_session)
):
    user = await db_session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_rating = rating.model_dump()
    db_rating["user_id"] = user_id
    stmt = insert(Rating).values(db_rating).on_conflict_do_update(constraint="pk_rating", set_=db_rating)
    await db_session.execute(stmt)
    await db_session.commit()
    return {"message": "rating updated"}

@router.delete("/{user_id}/ratings/{book_id}")
async def delete_rating(user_id: int, book_id: int, db_session: AsyncSession = Depends(get_db_session)):
    await db_session.execute(
        delete(Rating).where(and_(Rating.user_id == user_id, Rating.book_id == book_id))
    )
    await db_session.commit()
    return {"Message": "Deleted"}


@router.get("/{user_id}/reading_list", response_model=list[ReadingListEntrySchema])
async def get_user_reading_list(user_id: int, db_session: AsyncSession = Depends(get_db_session)):
    user = await db_session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.reading_list


@router.post("/{user_id}/reading_list")
async def add_new_reading_list_entry(
        user_id: int, new_entry: ReadingListEntrySchema, db_session: AsyncSession = Depends(get_db_session)
):
    user = await db_session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    reading_list_entry = ReadingList(user_id=user_id, book_id=new_entry.book_id, ranking=new_entry.ranking)
    user.reading_list.append(reading_list_entry)
    await db_session.commit()


@router.delete("/{user_id}/reading_list/{book_id}", status_code=status.HTTP_200_OK)
async def remove_book_from_reading_list(user_id: int, book_id: int, db_session: AsyncSession = Depends(get_db_session)):
    await db_session.execute(
        delete(ReadingList).where(and_(ReadingList.user_id == user_id, ReadingList.book_id == book_id))
    )
    await db_session.commit()
    return {"Message": "Deleted"}


@router.get("/{user_id}/recs", response_model=list[BookSchema])
async def get_user_recs(user_id: int, db_session: AsyncSession = Depends(get_db_session)):
    # TODO: Actually utilize a recommendation engine :)
    rec_ids = random.choices(range(1, 10001), k=25)
    books = await db_session.scalars(
        select(Book).where(Book.id.in_(rec_ids))
    )
    return books.all()
