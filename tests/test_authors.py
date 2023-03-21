from src.authors.router import (create_author, delete_author, get_author_by_id,
                                get_authors)
from src.database.schemas import AuthorCreate
from src.dependencies import get_db


def test_create_author(snapshot):
    snapshot.snapshot_dir = "snapshots/authors"
    value = create_author(
        AuthorCreate(**dict(id=99, name="Shakespeare")), db=next(get_db())
    )
    snapshot.assert_match(value.body, "create_author.json")


def test_get_authors(snapshot):
    snapshot.snapshot_dir = "snapshots/authors"
    values = get_authors(db=next(get_db()))
    snapshot.assert_match(values.body, "get_authors.json")


def test_get_author_by_id(snapshot):
    snapshot.snapshot_dir = "snapshots/authors"
    value = get_author_by_id(99, db=next(get_db()))
    snapshot.assert_match(value.body, "get_author_by_id.json")


def test_delete_author(snapshot):
    snapshot.snapshot_dir = "snapshots/authors"
    value = delete_author(99, db=next(get_db()))
    snapshot.assert_match(value.body, "delete_author.json")
