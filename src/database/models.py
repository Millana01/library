from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from src.database.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class UserBooks(BaseModel):
    __tablename__ = "user_books"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    count = Column(Integer)


class Books(BaseModel):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    author_id = Column(String, ForeignKey("authors.id"))
    total_count = Column(Integer)
    available_count = Column(Integer)


class Authors(BaseModel):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, index=True, unique=True)


class AuthorBooks(BaseModel):
    __tablename__ = "author_books"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
