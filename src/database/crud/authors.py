from sqlalchemy.orm import Session

from src.database.models import AuthorBooks, Authors
from src.database.schemas import AuthorCreate


class AuthorsQueries:
    @staticmethod
    def get_author_id_by_name(db: Session, name: str):
        return db.query(Authors.id).filter(Authors.name == name).scalar()

    @staticmethod
    def get_author_by_id(db: Session, author_id: int):
        return db.query(Authors).filter(Authors.id == author_id).first()

    @staticmethod
    def get_authors(db: Session, skip: int = 0, limit: int = 20):
        return db.query(Authors).offset(skip).limit(limit).all()

    @staticmethod
    def delete_author(db: Session, author_id: int):
        db.query(Authors).filter(Authors.id == author_id).delete()
        db.commit()

    @staticmethod
    def create_author(db: Session, author: AuthorCreate):
        db_author = Authors(name=author.name, id=author.id)
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author

    @staticmethod
    def create_author_books(db: Session, author_id: int, book_id: int):
        author_book = AuthorBooks(author_id=author_id, book_id=book_id)
        db.add(author_book)
        db.commit()
        db.refresh(author_book)
        return author_book

    @staticmethod
    def delete_author_books(db: Session, book_id: int):
        db.query(AuthorBooks).filter(AuthorBooks.book_id == book_id).delete()
        db.commit()
