from typing import List

from fastapi import status
from fastapi.exceptions import HTTPException

from src.database.crud.users import UserQueries
from src.database.models import User, UserBooks


class UserChecker:
    @staticmethod
    def check_user_not_exists(user_username: str) -> None:
        db_user = UserQueries().get_user_by_username(username=user_username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username already registered",
            )

    @staticmethod
    def check_user_exists(user_id: int) -> User:
        db_user = UserQueries().get_user(user_id=user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return db_user

    @staticmethod
    def check_user_books_exist(user_id: int) -> List[UserBooks]:
        user_books = UserQueries().get_user_books(user_id)
        if not user_books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no books on this user",
            )
        return user_books
