from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from models import Book, Genre, Rating
from models.book import book_genre_association
from schemas.book import BookDetailedSchema, BookSchema
from services.database import get_db_session

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get("/top_books", response_model=list[BookSchema])
async def get_top_n_books(
        n: Annotated[int, Query(le=50, ge=5)] = 10,
        db_session: AsyncSession = Depends(get_db_session)
):
    sub_query = select(
        Rating.book_id, func.avg(Rating.score).label("avg_rating"), func.count(Rating.book_id).label("rating_count")
    ).group_by(Rating.book_id).having(func.count(Rating.book_id) > 100).order_by(
        desc("avg_rating")
    ).limit(n).subquery()
    stmt = select(Book, sub_query.c.avg_rating).join(sub_query, sub_query.c.book_id == Book.id).order_by(
        desc(sub_query.c.avg_rating)
    )

    top_10_books = await db_session.scalars(stmt)
    return top_10_books.all()


@router.get("/{book_id}", response_model=BookDetailedSchema)
async def get_book(book_id: int, db_session: AsyncSession = Depends(get_db_session)):
    book = await Book.get_by_id(db_session, book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.get("", response_model=list[BookSchema])
async def search_books(
        q: Annotated[str, Query(min_length=1, max_length=100)],
        genre_filters: Annotated[list[str], None, Query()] = None,
        min_pages: Annotated[int, None, Query(gt=0)] = None,
        max_pages: Annotated[int, None, Query(gt=0)] = None,
        db_session: AsyncSession = Depends(get_db_session)
):
    stmt = select(Book).where(Book.title.match(q))
    if genre_filters:
        stmt = stmt.where(Book.genres.any(Genre.name.in_(genre_filters)))
    if min_pages:
        stmt = stmt.where(Book.pages >= min_pages)
    if max_pages:
        stmt = stmt.where(Book.pages <= max_pages)
    result = await db_session.scalars(stmt)
    return result.all()
