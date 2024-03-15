from src.database import Base
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from datetime import datetime


class Book(Base):
    __tablename__ = 'books'

    book_id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    publication_year = Column(Integer)
    genre = Column(String(50))
    description = Column(Text)

    reviews = relationship('Review', back_populates='book')



class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = Column(Integer, ForeignKey('books.book_id'), nullable=False)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="reviews")
    book: Mapped["Book"] = relationship("Book", back_populates="reviews")

