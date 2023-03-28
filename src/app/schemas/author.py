from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    id: Optional[int]


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True
