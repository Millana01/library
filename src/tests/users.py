from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/books/create",
        json={
            "title": "War and Peace",
            "description": "Novel",
            "total_count": 20,
            "author": "Tolstoy",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    r_json: dict = response.json()
    exp_fields = ("id", "title", "description", "author_id", "available_count")
    assert exp_fields in r_json


def test_get_users():
    response = client.get("/users", params={"skip": 0, "limit": 3})
    assert response.status_code == status.HTTP_200_OK
    r_json: dict = response.json()
    assert len(r_json) <= 3
    exp_fields = ("id", "username", "is_active")
    for resp in r_json:
        assert exp_fields in resp
