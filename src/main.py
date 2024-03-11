from fastapi import FastAPI, Depends
import uvicorn
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.models import Book
from src.database import get_session

app = FastAPI(
    title="Books app"
)

@app.get("/")
async def get_books(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book))
    return result.scalars().all()


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
