from typing import List, Union

from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from src.database.crud.authors import AuthorsQueries
from src.database.crud.books import BooksQueries
from src.database.crud.users import UserQueries
from src.database.schemas import Author, AuthorCreate

from .checkers import AuthorChecker

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.post("/create")
def create_author(
    authors: Union[AuthorCreate, List[AuthorCreate]]
) -> Union[Author, List[Author]]:
    if isinstance(authors, list):
        authors_create = []
        for author in authors:
            AuthorChecker.check_author_not_exists(author.name)
            authors_create.append(AuthorsQueries().create_author(author))
        return authors_create
    AuthorChecker.check_author_not_exists(authors.name)
    return AuthorsQueries().create_author(authors)


@router.get("")
def get_authors(skip: int = 0, limit: int = 20) -> List:
    return AuthorsQueries().get_authors(skip, limit)


@router.get("/{author_id}", response_model=Author)
def get_author_by_id(author_id: int):
    author = AuthorChecker.check_author_exists(author_id)
    return author


@router.delete("/{author_id}")
def delete_author(author_id: int) -> Response:
    AuthorChecker.check_author_exists(author_id)
    books = BooksQueries().get_books_by_author_id(author_id)
    if books:
        for book in books:
            user_book = UserQueries().get_user_book_by_book_id(book.id)
            if user_book:
                UserQueries().delete_user_book(book.id, user_book.user_id)
            AuthorsQueries().delete_author_books(book.id)
            BooksQueries().delete_book(book.id)
    AuthorsQueries().delete_author(author_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Author with id={author_id} deleted"},
    )
