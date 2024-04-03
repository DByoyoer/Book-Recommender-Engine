from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import Book
from schemas.book import BookSchema
from services.database import get_db_session

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get("/{book_id}", response_model=BookSchema)
async def get_book(book_id: int, db_session: AsyncSession = Depends(get_db_session)):
    book = await Book.get_by_id(db_session, book_id)
    return book

