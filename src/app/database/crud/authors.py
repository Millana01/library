from typing import List

from sqlalchemy.orm import Session

from src.app.database.models import AuthorBooks, Authors
from src.app.schemas.author import AuthorCreate


def get_author_id_by_name(db: Session, name: str):
    return db.query(Authors.id).filter(Authors.name == name).scalar()


def get_authors_by_names(db: Session, names: list):
    return db.query(Authors.id).filter(Authors.name.in_(names)).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(Authors).filter(Authors.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Authors).offset(skip).limit(limit).all()


def delete_author(db: Session, author_id: int):
    db.query(Authors).filter(Authors.id == author_id).delete()
    db.commit()


def create_author(db: Session, author: AuthorCreate):
    db_author = Authors(name=author.name, id=author.id)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_authors(db: Session, authors: List[AuthorCreate]):
    db_authors = [Authors(name=author.name, id=author.id) for author in authors]
    db.bulk_save_objects(db_authors, return_defaults=True)
    db.commit()
    return db_authors


def create_author_books(db: Session, author_id: int, book_id: int):
    author_book = AuthorBooks(author_id=author_id, book_id=book_id)
    db.add(author_book)
    db.commit()
    db.refresh(author_book)
    return author_book


def delete_author_book(db: Session, book_id: int):
    db.query(AuthorBooks).filter(AuthorBooks.book_id == book_id).delete()
    db.commit()


def delete_author_books(db: Session, book_ids: list):
    db.query(AuthorBooks).filter(AuthorBooks.book_id.in_(book_ids)).delete()
    db.commit()
