from pydantic import BaseModel


class BookModel(BaseModel):
    title: str
    author: str
    publication_year: int | None = None
    genre: str | None = None
    description: str | None = None