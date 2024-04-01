from fastapi import FastAPI, Depends
import uvicorn
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis import asyncio as aioredis
from contextlib import asynccontextmanager

from config import REDIS_HOST, REDIS_PORT
from users.routers import router as user_router
from books.routers import router as book_router
from tasks.routers import router as report_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title="Books app",
    lifespan=lifespan
)


app.include_router(user_router)
app.include_router(book_router)
app.include_router(report_router)



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
