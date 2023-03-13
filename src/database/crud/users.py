from src.database import base
from src.database.base import LibraryDB
from src.database.models import Books, User, UserBooks
from src.database.schemas import UserCreate
from src.helpers.singleton import Singleton


class UserQueries(metaclass=Singleton):
    def __init__(self, db: base.BaseDB = None):
        self.db = db or LibraryDB()

    def get_user(self, user_id: int):
        with self.db.create_session() as session:
            return session.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str):
        with self.db.create_session() as session:
            return session.query(User).filter(User.username == username).first()

    def get_users(self, skip: int = 0, limit: int = 20):
        with self.db.create_session() as session:
            return session.query(User).offset(skip).limit(limit).all()

    def get_user_books(self, user_id: int):
        with self.db.create_session() as session:
            return (
                session.query(UserBooks.book_id, UserBooks.count, Books)
                .join(Books, UserBooks.book_id == Books.id)
                .filter(UserBooks.user_id == user_id)
                .all()
            )

    def get_user_book_by_book_id(self, book_id: int):
        with self.db.create_session() as session:
            return session.query(UserBooks).filter(UserBooks.book_id == book_id).first()

    def create_user(self, user: UserCreate):
        with self.db.create_session() as session:
            db_user = User(username=user.username, hashed_password=user.password)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    def create_user_books(self, user_id: int, book_id: int):
        with self.db.create_session() as session:
            user_book = UserBooks(user_id=user_id, book_id=book_id, count=1)
            session.add(user_book)
            session.commit()
            session.refresh(user_book)
            return user_book

    def delete_user_book(self, book_id: int, user_id: int):
        with self.db.create_session() as session:
            session.query(UserBooks).filter(
                UserBooks.book_id == book_id, UserBooks.user_id == user_id
            ).delete()
            session.commit()

    def update_user_book_count(self, user_book_id: int, count: int):
        with self.db.create_session() as session:
            session.query(UserBooks).filter(UserBooks.id == user_book_id).update(
                {UserBooks.count: count}
            )
