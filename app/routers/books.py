from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import Book
from schemas.book import BookDetailedSchema
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
