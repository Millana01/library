from typing import List

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from src.auth.dependencies import get_current_active_user, get_password_hash
from src.books.checkers import BookChecker
from src.database.crud import books, users
from src.database.schemas import User, UserCreate

from .checkers import UserChecker

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("")
def get_users(skip: int = 0, limit: int = 20) -> List:
    return [
        User(**user.__dict__) for user in users.UserQueries().get_users(skip, limit)
    ]


@router.get("/me", response_model=User)
async def get_users_me(current_user: User = Depends(get_current_active_user)):
    db_user = UserChecker.check_user_exists(current_user.id)
    return db_user


@router.post("/create", response_model=User)
def create_user(user: UserCreate):
    UserChecker.check_user_not_exists(user.username)
    user.password = get_password_hash(user.password)
    return users.UserQueries().create_user(user=user)


@router.get("/books")
async def get_user_books(current_user: User = Depends(get_current_active_user)):
    user_books = UserChecker.check_user_books_exist(current_user.id)
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
    book_id: int, current_user: User = Depends(get_current_active_user)
) -> Response:
    available_count = BookChecker.check_books_available_count(book_id).available_count
    available_count -= 1
    books.BooksQueries().update_available_count(book_id, available_count)
    user_book = users.UserQueries().get_user_book_by_book_id(book_id)
    if user_book:
        user_book.count += 1
        users.UserQueries().update_user_book_count(user_book.id, user_book.count)
    else:
        users.UserQueries().create_user_books(current_user.id, book_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "You reserve a book"}
    )


@router.put("/book/return")
async def return_book(
    book_id: int, current_user: User = Depends(get_current_active_user)
) -> Response:
    UserChecker.check_user_books_exist(current_user.id)
    available_count = BookChecker.check_books_available_total_count(
        book_id
    ).available_count
    available_count += 1
    books.BooksQueries().update_available_count(book_id, available_count)
    user_book = users.UserQueries().get_user_book_by_book_id(book_id)
    if user_book.count > 1:
        user_book.count -= 1
        users.UserQueries().update_user_book_count(user_book.id, user_book.count)
    else:
        users.UserQueries().delete_user_book(book_id, current_user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "You return a book"}
    )
