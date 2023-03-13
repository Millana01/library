from fastapi import status
from fastapi.exceptions import HTTPException

from src.database.crud.authors import AuthorsQueries
from src.database.models import Authors


class AuthorChecker:
    @staticmethod
    def check_author_exists(author_id: int) -> Authors:
        author = AuthorsQueries().get_author_by_id(author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Author with such id doesn't exist",
            )
        return author

    @staticmethod
    def check_author_exists_by_name(author_name: str) -> int:
        author_id = AuthorsQueries().get_author_id_by_name(author_name)
        if not author_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Author with such name doesn't exist",
            )
        return author_id

    @staticmethod
    def check_author_not_exists(author_name: str) -> None:
        author_id = AuthorsQueries().get_author_id_by_name(author_name)
        if author_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Author is already exist in system",
            )
