import asyncio
import os
import sys
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.pool import NullPool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from books.models import Book, Review
from config import (TEST_DB_HOST, TEST_DB_NAME, TEST_DB_PASS, TEST_DB_PORT,
                    TEST_DB_USER)
from database import Base, get_session
from main import app
from users.auth import get_current_user
from users.models import User

# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool, echo=True)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_session] = override_get_async_session

@pytest_asyncio.fixture(autouse=True, scope='session')
async def create_test_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
#
# client = TestClient(app)

@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def test_user() -> User:
    async with async_session_maker() as session:
        fake_user = User(
            username="fake_user",
            email='test@example.com',
            hashed_password='fake_hashed_password',
        )
        session.add(fake_user)
        await session.commit()
        await session.refresh(fake_user)
        return fake_user


@pytest_asyncio.fixture
async def test_book() -> Book:
    async with async_session_maker() as session:
        fake_book = Book(
            # book_id=1,
            title='something',
            author='something',
            publication_year=2024,
            genre='something',
            description='something',
        )
        session.add(fake_book)
        await session.commit()
        await session.refresh(fake_book)
        return fake_book


@pytest_asyncio.fixture
async def test_review() -> Review:
    async with async_session_maker() as session:
        fake_review = Review(
            # review_id=1,
            book_id=1,
            user_id=1,
            text='some review',
        )
        session.add(fake_review)
        await session.commit()
        await session.refresh(fake_review)
        return fake_review


@pytest_asyncio.fixture
def override_get_current_user(test_user: User):
    def _get_current_user():
        return test_user
    app.dependency_overrides[get_current_user] = _get_current_user
    yield
    app.dependency_overrides.pop(get_current_user)