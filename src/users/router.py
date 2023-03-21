from typing import List

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_active_user, get_password_hash
from src.books.checkers import BookChecker
from src.database.crud import books, users
from src.database.schemas import User, UserCreate
from src.dependencies import get_db

from .checkers import UserChecker

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("")
def get_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)) -> List:
    return [
        User(**user.__dict__) for user in users.UserQueries.get_users(db, skip, limit)
    ]


@router.get("/me", response_model=User)
async def get_users_me(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    db_user = UserChecker.check_user_exists(db, current_user.id)
    return db_user


@router.post("/create", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    UserChecker.check_user_not_exists(db, user.username)
    user.password = get_password_hash(user.password)
    return users.UserQueries.create_user(db, user=user)


@router.get("/books")
async def get_user_books(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    user_books = UserChecker.check_user_books_exist(db, current_user.id)
    books_ = []
    for result in user_books:
        book_id, count, info = result
        books_.append(
            {
                "id": book_id,
                "title": info.title,
                "description": info.description,
                "author_id": info.author_id,
                "count": count,
            }
        )
    return books_


@router.put("/book/reserve")
async def reserve_book(
    book_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Response:
    available_count = BookChecker.check_books_available_count(
        db, book_id
    ).available_count
    available_count -= 1
    books.BooksQueries.update_available_count(db, book_id, available_count)
    user_book = users.UserQueries.get_user_book_by_book_id(db, book_id)
    if user_book:
        user_book.count += 1
        users.UserQueries.update_user_book_count(db, user_book.id, user_book.count)
    else:
        users.UserQueries.create_user_books(db, current_user.id, book_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "You reserve a book"}
    )


@router.put("/book/return")
async def return_book(
    book_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Response:
    UserChecker.check_user_books_exist(db, current_user.id)
    available_count = BookChecker.check_books_available_total_count(
        db, book_id
    ).available_count
    available_count += 1
    books.BooksQueries.update_available_count(db, book_id, available_count)
    user_book = users.UserQueries.get_user_book_by_book_id(db, book_id)
    if user_book.count > 1:
        user_book.count -= 1
        users.UserQueries.update_user_book_count(db, user_book.id, user_book.count)
    else:
        users.UserQueries.delete_user_book(db, book_id, current_user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "You return a book"}
    )
