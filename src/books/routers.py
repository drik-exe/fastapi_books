import time
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from books.models import Book, Review
from books.schemas import BookModel
from database import get_session
from users.auth import get_current_user
from users.models import User

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post("/create")
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
        print(e)
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


@router.post("/review/{book_id}")
async def create_review(
        book_id: int,
        review_text: str,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)):
    try:
        query = select(Book).where(Book.book_id == book_id)
        results = await session.execute(query)
        book = results.scalar_one_or_none()
        if book is None:
            raise HTTPException(status_code=400, detail="books does not exist")

        review = Review(
            book_id=book.book_id,
            user_id=current_user.user_id,
            text=review_text
        )
        session.add(review)
        await session.commit()
        return {"review": review}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await session.close()


@router.get("/check-users-reviews")
async def check_users_reviews(
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)):
    try:
        query = select(Review).where(Review.user_id == current_user.user_id)
        results = await session.execute(query)
        reviews = results.scalar()
        await session.commit()
        return {"review": reviews}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await session.close()


@router.get("/check-books-reviews/{book_id}")
async def check_books_reviews(
        book_id: int,
        session: AsyncSession = Depends(get_session)):
    try:
        query = select(Review).where(Review.book_id == book_id)
        results = await session.execute(query)
        reviews = results.scalar()
        await session.commit()
        return {"reviews": reviews}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await session.close()



@router.put("/update-review/{review_id}")
async def update_review(
        review_id: int,
        new_text: str,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)):
    async with session.begin():
        review = await session.get(Review, review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Comment not found")
        if review.user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this comment")

        review.text = new_text
        await session.commit()
        return {"review": review}


@router.get("/book-of-the-week")
@cache(expire=10)
async def get_book_of_the_week(session: AsyncSession = Depends(get_session)):
    week_ago = datetime.utcnow() - timedelta(days=7)
    try:
        query = select(
                Book, func.count(Review.review_id).label("review_count")
            ).join(
                Review, Review.book_id == Book.book_id
            ).filter(
                Review.created_at >= week_ago
            ).group_by(
                Book.book_id
            ).order_by(
                desc("review_count")
            ).limit(1)
        results = await session.execute(query)
        time.sleep(2)
        most_commented_book = results.scalar_one_or_none()
        if most_commented_book is None:
            raise HTTPException(status_code=400, detail="No book for this week")
        return {"book of the week": most_commented_book}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await session.close()
