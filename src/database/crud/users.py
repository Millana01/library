from sqlalchemy.orm import Session

from src.database.models import Books, User, UserBooks
from src.database.schemas import UserCreate


class UserQueries:
    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 20):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def get_user_books(db: Session, user_id: int):
        return (
            db.query(UserBooks.book_id, UserBooks.count, Books)
            .join(Books, UserBooks.book_id == Books.id)
            .filter(UserBooks.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_user_book_by_book_id(db: Session, book_id: int):
        return db.query(UserBooks).filter(UserBooks.book_id == book_id).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        db_user = User(username=user.username, hashed_password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def create_user_books(db: Session, user_id: int, book_id: int):
        user_book = UserBooks(user_id=user_id, book_id=book_id, count=1)
        db.add(user_book)
        db.commit()
        db.refresh(user_book)
        return user_book

    @staticmethod
    def delete_user_book(db: Session, book_id: int, user_id: int):
        db.query(UserBooks).filter(
            UserBooks.book_id == book_id, UserBooks.user_id == user_id
        ).delete()
        db.commit()

    @staticmethod
    def update_user_book_count(db: Session, user_book_id: int, count: int):
        db.query(UserBooks).filter(UserBooks.id == user_book_id).update(
            {UserBooks.count: count}
        )
