from typing import List, Union

from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database.crud.authors import AuthorsQueries
from src.database.crud.books import BooksQueries
from src.database.crud.users import UserQueries
from src.database.schemas import Author, AuthorCreate
from src.dependencies import get_db

from .checkers import AuthorChecker

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.post("/create")
def create_author(
    authors: Union[AuthorCreate, List[AuthorCreate]], db: Session = Depends(get_db)
) -> Response:
    if isinstance(authors, list):
        authors_create = []
        for author in authors:
            AuthorChecker.check_author_not_exists(db, author.name)
            authors_create.append(
                jsonable_encoder(AuthorsQueries.create_author(db, author))
            )
        return JSONResponse(content=authors_create)
    AuthorChecker.check_author_not_exists(db, authors.name)
    return JSONResponse(
        content=jsonable_encoder(AuthorsQueries.create_author(db, authors))
    )


@router.get("")
def get_authors(
    skip: int = 0, limit: int = 20, db: Session = Depends(get_db)
) -> Response:
    authors = AuthorsQueries.get_authors(db, skip, limit)
    content = [jsonable_encoder(author) for author in authors]
    return JSONResponse(content=content)


@router.get("/{author_id}", response_model=Author)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = AuthorChecker.check_author_exists(db, author_id)
    return JSONResponse(content=jsonable_encoder(author))


@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)) -> Response:
    AuthorChecker.check_author_exists(db, author_id)
    books = BooksQueries.get_books_by_author_id(db, author_id)
    if books:
        for book in books:
            user_book = UserQueries.get_user_book_by_book_id(db, book.id)
            if user_book:
                UserQueries.delete_user_book(db, book.id, user_book.user_id)
            AuthorsQueries.delete_author_books(db, book.id)
            BooksQueries.delete_book(db, book.id)
    AuthorsQueries.delete_author(db, author_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Author with id={author_id} deleted"},
    )
