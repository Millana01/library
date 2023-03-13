from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_book():
    response = client.post(
        "/books/create",
        json={
            "title": "War and Peace",
            "description": "Novel",
            "total_count": 20,
            "author": "Tolstoy",
        },
    )
    assert response.status_code == 200
    r_json: dict = response.json()
    exp_fields = ("id", "title", "description", "author_id", "available_count")
    assert exp_fields in r_json


def test_get_books():
    response = client.get("/books", params={"skip": 0, "limit": 3})
    assert response.status_code == 200
    r_json: dict = response.json()
    assert len(r_json) <= 3
    exp_fields = (
        "id",
        "title",
        "description",
        "author_id",
        "total_count",
        "available_count",
    )
    for resp in r_json:
        assert exp_fields in resp


def test_get_book_by_id():
    response = client.get("/books/2")
    assert response.status_code == 200
    r_json: dict = response.json()
    exp_fields = ("id", "title", "description", "author_id", "available_count")
    assert exp_fields in r_json


def test_delete_book():
    response = client.delete("/books/2")
    assert response.status_code == 200
    assert response.json() == {"message": "Book with id=2 deleted"}
