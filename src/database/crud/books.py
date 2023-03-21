from sqlalchemy.orm import Session

from src.database.models import Books
from src.database.schemas import BooksCreate


class BooksQueries:
    @staticmethod
    def get_book_by_id(db: Session, book_id: int):
        return db.query(Books).filter(Books.id == book_id).first()

    @staticmethod
    def get_books_by_author_id(db: Session, author_id: int):
        return db.query(Books).filter(Books.author_id == author_id).all()

    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 20):
        return db.query(Books).offset(skip).limit(limit).all()

    @staticmethod
    def get_book_by_title_and_author_id(db: Session, title: str, author_id: int):
        return (
            db.query(Books.id)
            .filter(Books.title == title, Books.author_id == author_id)
            .scalar()
        )

    @staticmethod
    def create_book(db: Session, book: BooksCreate):
        db_book = Books(
            title=book.title,
            description=book.description,
            author_id=book.author,
            total_count=book.total_count,
            available_count=book.total_count,
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def delete_book(db: Session, book_id: int):
        db.query(Books).filter(Books.id == book_id).delete()
        db.commit()

    @staticmethod
    def update_available_count(db: Session, book_id: int, available_count: int):
        db.query(Books).filter(Books.id == book_id).update(
            {Books.available_count: available_count}
        )
