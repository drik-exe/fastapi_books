from fastapi import FastAPI, Depends
import uvicorn
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import engine, Base
from src.users.routers import router as user_router



app = FastAPI(
    title="Books app"
)

# @app.on_event("startup")
# async def startup_event():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

app.include_router(user_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
