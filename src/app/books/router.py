from typing import List

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.app.authors import checkers as authors_checker
from src.app.books import checkers as book_checker
from src.app.database.crud import authors as authors_queries
from src.app.database.crud import books as books_queries
from src.app.database.dependencies import get_db
from src.app.schemas.book import Books, BooksCreate

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.post("/create", response_model=Books)
def create_book(book: BooksCreate, db: Session = Depends(get_db)):
    author_id = authors_checker.check_author_exists_by_name(db, book.author)
    book_checker.check_book_not_exists(db, author_id, book.title)
    book.author = author_id
    book = books_queries.create_book(db, book=book)
    authors_queries.create_author_books(db, author_id, book.id)
    return book


@router.get("")
def get_books(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)) -> List:
    return books_queries.get_books(db, skip, limit)


@router.get("/{book_id}", response_model=Books)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = book_checker.check_book_exists(db, book_id)
    return book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)) -> Response:
    book_checker.check_book_exists(db, book_id)
    authors_queries.delete_author_book(db, book_id)
    books_queries.delete_book(db, book_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Book with id={book_id} deleted"},
    )
