from typing import List, Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.app.database.crud import users as users_queries
from src.app.database.models.users import User, UserBooks


def check_user_not_exists(db: Session, user_username: str) -> None:
    db_user = users_queries.get_user_by_username(db, username=user_username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username already registered",
        )


def check_user_exists(db: Session, user_id: int) -> User:
    db_user = users_queries.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


def check_user_books_exist(db: Session, user_id: int) -> List[UserBooks]:
    user_books = users_queries.get_user_books(db, user_id)
    if not user_books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no books on this user",
        )
    return user_books


def check_user_book_by_book_id(db: Session, book_id: int) -> Optional[UserBooks]:
    user_book = users_queries.get_user_book_by_book_id(db, book_id)
    if not user_book:
        return None
    return user_book
