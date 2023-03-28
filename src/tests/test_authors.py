from src.app.authors.router import (
    create_author,
    delete_author,
    get_author_by_id,
    get_authors,
)
from src.app.schemas.author import AuthorCreate
from src.tests.db_session import SessionMixin


def test_create_author(snapshot):
    snapshot.snapshot_dir = "snapshots/authors"
    session = SessionMixin().session()
    value = create_author(AuthorCreate(**dict(id=99, name="Shakespeare")), db=session)
    snapshot.assert_match(value.body, "create_author.json")


def test_get_authors(snapshot):
    snapshot.snapshot_dir = "snapshots/authors"
    session = SessionMixin().session()
    values = get_authors(db=session)
    snapshot.assert_match(values.body, "get_authors.json")


def test_get_author_by_id(snapshot):
    snapshot.snapshot_dir = "snapshots/authors"
    session = SessionMixin().session()
    value = get_author_by_id(99, db=session)
    snapshot.assert_match(value.body, "get_author_by_id.json")


def test_delete_author(snapshot):
    snapshot.snapshot_dir = "snapshots/authors"
    session = SessionMixin().session()
    value = delete_author(99, db=session)
    snapshot.assert_match(value.body, "delete_author.json")
