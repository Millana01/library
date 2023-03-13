from src.database import base
from src.database.base import LibraryDB
from src.database.models import Books
from src.database.schemas import BooksCreate
from src.helpers.singleton import Singleton


class BooksQueries(metaclass=Singleton):
    def __init__(self, db: base.BaseDB = None):
        self.db = db or LibraryDB()

    def get_book_by_id(self, book_id: int):
        with self.db.create_session() as session:
            return session.query(Books).filter(Books.id == book_id).one()

    def get_books_by_author_id(self, author_id: int):
        with self.db.create_session() as session:
            return session.query(Books).filter(Books.author_id == author_id).all()

    def get_books(self, skip: int = 0, limit: int = 20):
        with self.db.create_session() as session:
            return session.query(Books).offset(skip).limit(limit).all()

    def get_book_by_title_and_author_id(self, title: str, author_id: int):
        with self.db.create_session() as session:
            return (
                session.query(Books.id)
                .filter(Books.title == title, Books.author_id == author_id)
                .scalar()
            )

    def create_book(self, book: BooksCreate):
        with self.db.create_session() as session:
            db_book = Books(
                title=book.title,
                description=book.description,
                author_id=book.author,
                total_count=book.total_count,
                available_count=book.total_count,
            )
            session.add(db_book)
            session.commit()
            session.refresh(db_book)
            return db_book

    def delete_book(self, book_id: int):
        with self.db.create_session() as session:
            session.query(Books).filter(Books.id == book_id).delete()
            session.commit()

    def update_available_count(self, book_id: int, available_count: int):
        with self.db.create_session() as session:
            session.query(Books).filter(Books.id == book_id).update(
                {Books.available_count: available_count}
            )
