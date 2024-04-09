import os
import sys

import pytest
from httpx import AsyncClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from books.models import Book, Review
from users.models import User


@pytest.mark.asyncio
async def test_create_book(ac: AsyncClient):
    response = await ac.post("/books/create", json={
        "title": "string",
        "author": "string",
        "publication_year": 0,
        "genre": "string",
        "description": "string"
    })

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_search_books(ac: AsyncClient):
    response = await ac.get("/books/search/{title}", params={"title": "string"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_review(ac: AsyncClient, test_book: Book, test_user: User, override_get_current_user):
    response = await ac.post(f"/books/review/{test_book.book_id}?review_text=Great book!")
    print(response.json())
    assert response.status_code == 200
    assert 'review_id' in response.json()['review']



@pytest.mark.asyncio
async def test_check_books_reviews(ac: AsyncClient, test_book: Book):
    response = await ac.get(f"/books/check-books-reviews/{test_book.book_id}")
    assert response.status_code == 200
    assert 'reviews' in response.json()






