from typing import List, Union

from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.app.authors import checkers
from src.app.database.crud import authors as authors_queries
from src.app.database.crud import books as books_queries
from src.app.database.crud import users as users_queries
from src.app.database.dependencies import get_db
from src.app.schemas.author import Author, AuthorCreate

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
        checkers.check_authors_not_exist(db, [author.name for author in authors])
        authors_create.append(
            jsonable_encoder(authors_queries.create_authors(db, authors))
        )
        return JSONResponse(content=authors_create)
    checkers.check_author_not_exists(db, authors.name)
    return JSONResponse(
        content=jsonable_encoder(authors_queries.create_author(db, authors))
    )


@router.get("")
def get_authors(
    skip: int = 0, limit: int = 20, db: Session = Depends(get_db)
) -> Response:
    authors = authors_queries.get_authors(db, skip, limit)
    content = [jsonable_encoder(author) for author in authors]
    return JSONResponse(content=content)


@router.get("/{author_id}", response_model=Author)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = checkers.check_author_exists(db, author_id)
    return JSONResponse(content=jsonable_encoder(author))


@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)) -> Response:
    checkers.check_author_exists(db, author_id)
    books = books_queries.get_books_by_author_id(db, author_id)
    if books:
        book_ids = [book.id for book in books]
        user_books = users_queries.get_user_books_by_book_ids(db, book_ids)
        if user_books:
            user_book_ids = [user_book.user_id for user_book in user_books]
            users_queries.delete_user_books(db, book_ids, user_book_ids)
        authors_queries.delete_author_books(db, book_ids)
        books_queries.delete_books(db, book_ids)
    authors_queries.delete_author(db, author_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Author with id={author_id} deleted"},
    )
