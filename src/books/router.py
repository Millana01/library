from typing import List

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.authors.checkers import AuthorChecker
from src.database.crud import authors, books
from src.database.schemas import Books, BooksCreate
from src.dependencies import get_db

from .checkers import BookChecker

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.post("/create", response_model=Books)
def create_book(book: BooksCreate, db: Session = Depends(get_db)):
    author_id = AuthorChecker.check_author_exists_by_name(db, book.author)
    BookChecker.check_book_not_exists(db, author_id, book.title)
    book.author = author_id
    book = books.BooksQueries.create_book(db, book=book)
    authors.AuthorsQueries.create_author_books(db, author_id, book.id)
    return book


@router.get("")
def get_books(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)) -> List:
    return books.BooksQueries.get_books(db, skip, limit)


@router.get("/{book_id}", response_model=Books)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = BookChecker.check_book_exists(db, book_id)
    return book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)) -> Response:
    BookChecker.check_book_exists(db, book_id)
    authors.AuthorsQueries.delete_author_books(db, book_id)
    books.BooksQueries.delete_book(db, book_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Book with id={book_id} deleted"},
    )
