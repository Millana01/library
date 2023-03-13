from typing import Optional, Union

from pydantic import BaseModel


class BookBase(BaseModel):
    title: Optional[str]
    description: Union[str, None] = None


class BooksCreate(BookBase):
    total_count: int
    author: str


class Books(BookBase):
    id: int
    author_id: int
    available_count: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    ...


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True
