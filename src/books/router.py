from typing import List

from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from src.authors.checkers import AuthorChecker
from src.database.crud import authors, books
from src.database.schemas import Books, BooksCreate

from .checkers import BookChecker

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.post("/create", response_model=Books)
def create_book(book: BooksCreate):
    author_id = AuthorChecker.check_author_exists_by_name(book.author)
    BookChecker.check_book_not_exists(author_id, book.title)
    book.author = author_id
    book = books.BooksQueries().create_book(book=book)
    authors.AuthorsQueries().create_author_books(author_id, book.id)
    return book


@router.get("")
def get_books(skip: int = 0, limit: int = 20) -> List:
    return books.BooksQueries().get_books(skip, limit)


@router.get("/{book_id}", response_model=Books)
def get_book_by_id(book_id: int):
    book = BookChecker.check_book_exists(book_id)
    return book


@router.delete("/{book_id}")
def delete_book(book_id: int) -> Response:
    BookChecker.check_book_exists(book_id)
    authors.AuthorsQueries().delete_author_books(book_id)
    books.BooksQueries().delete_book(book_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Book with id={book_id} deleted"},
    )
