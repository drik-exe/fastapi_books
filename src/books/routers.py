from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.models import Book
from src.books.schemas import BookModel
from src.database import get_session

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post("/create", response_model=BookModel)
async def create_book(
        book: BookModel,
        session: AsyncSession = Depends(get_session)):
    try:
        new_book = Book(
            title=book.title,
            author=book.author,
            publication_year=book.publication_year,
            genre=book.genre,
            description=book.description
        )
        session.add(new_book)
        await session.commit()
        return {"book": new_book}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await session.close()


@router.get("/search/{title}")
async def search_books(
        title: str,
        session: AsyncSession = Depends(get_session)):
    try:
        query = select(Book).where(Book.title == title)
        results = await session.execute(query)
        books = results.scalars().all()
        await session.commit()
        return {"books": books}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await session.close()