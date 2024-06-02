from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Book, Genre
from models.book import book_genre_association
from schemas.book import BookDetailedSchema, BookSchema
from services.database import get_db_session

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get("/{book_id}", response_model=BookDetailedSchema)
async def get_book(book_id: int, db_session: AsyncSession = Depends(get_db_session)):
    book = await Book.get_by_id(db_session, book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.get("/", response_model=list[BookSchema])
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
