from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.database.crud.books import BooksQueries
from src.database.models import Books


class BookChecker:
    @staticmethod
    def check_book_not_exists(db: Session, author_id: int, book_title: str) -> None:
        db_book = BooksQueries.get_book_by_title_and_author_id(
            db, title=book_title, author_id=author_id
        )
        if db_book:
            raise HTTPException(
                status_code=400, detail="Book is already exist in system"
            )

    @staticmethod
    def check_book_exists(db: Session, book_id: int) -> Books:
        book = BooksQueries.get_book_by_id(db, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with such id doesn't exist",
            )
        return book

    @staticmethod
    def check_books_available_count(db: Session, book_id: int) -> Books:
        book = BookChecker.check_book_exists(db, book_id)
        if book.available_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no available books, choose another one",
            )
        return book

    @staticmethod
    def check_books_available_total_count(db: Session, book_id: int) -> Books:
        book = BookChecker.check_book_exists(db, book_id)
        if book.available_count == book.total_count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There are all books in library",
            )
        return book
