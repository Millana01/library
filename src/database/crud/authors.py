from src.database import base
from src.database.base import LibraryDB
from src.database.models import AuthorBooks, Authors
from src.database.schemas import AuthorCreate
from src.helpers.singleton import Singleton


class AuthorsQueries(metaclass=Singleton):
    def __init__(self, db: base.BaseDB = None):
        self.db = db or LibraryDB()

    def get_author_id_by_name(self, name: str):
        with self.db.create_session() as session:
            return session.query(Authors.id).filter(Authors.name == name).scalar()

    def get_author_by_id(self, author_id: int):
        with self.db.create_session() as session:
            return session.query(Authors).filter(Authors.id == author_id).first()

    def get_authors(self, skip: int = 0, limit: int = 20):
        with self.db.create_session() as session:
            return session.query(Authors).offset(skip).limit(limit).all()

    def delete_author(self, author_id: int):
        with self.db.create_session() as session:
            session.query(Authors).filter(Authors.id == author_id).delete()
            session.commit()

    def create_author(self, author: AuthorCreate):
        with self.db.create_session() as session:
            db_author = Authors(name=author.name)
            session.add(db_author)
            session.commit()
            session.refresh(db_author)
            return db_author

    def create_author_books(self, author_id: int, book_id: int):
        with self.db.create_session() as session:
            author_book = AuthorBooks(author_id=author_id, book_id=book_id)
            session.add(author_book)
            session.commit()
            session.refresh(author_book)
            return author_book

    def delete_author_books(self, book_id: int):
        with self.db.create_session() as session:
            session.query(AuthorBooks).filter(AuthorBooks.book_id == book_id).delete()
            session.commit()
