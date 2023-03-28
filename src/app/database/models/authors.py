from sqlalchemy import Column, ForeignKey, Integer, String

from src.app.database.base import BaseModel


class Authors(BaseModel):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, index=True, unique=True)


class AuthorBooks(BaseModel):
    __tablename__ = "author_books"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
