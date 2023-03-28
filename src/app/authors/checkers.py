from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.app.database.crud import authors
from src.app.database.models import Authors


def check_author_exists(db: Session, author_id: int) -> Authors:
    author = authors.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with such id doesn't exist",
        )
    return author


def check_author_exists_by_name(db: Session, author_name: str) -> int:
    author_id = authors.get_author_id_by_name(db, author_name)
    if not author_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with such name doesn't exist",
        )
    return author_id


def check_author_not_exists(db: Session, author_name: str) -> None:
    author_id = authors.get_author_id_by_name(db, author_name)
    if author_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author is already exist in system",
        )


def check_authors_not_exist(db: Session, author_names: list) -> None:
    author_ids = authors.get_authors_by_names(db, author_names)
    if author_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authors with ids {author_ids} are already exist in system",
        )
