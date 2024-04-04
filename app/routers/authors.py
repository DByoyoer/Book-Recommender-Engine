from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Author
from schemas.book import AuthorFullSchema
from services.database import get_db_session

router = APIRouter(
    prefix="/authors",
    tags=["authors"],

)

@router.get("/{author_id}", response_model=AuthorFullSchema)
async def get_author(author_id:int, db_session: AsyncSession = Depends(get_db_session)):
    result = await db_session.get(Author, author_id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Author not found.")
