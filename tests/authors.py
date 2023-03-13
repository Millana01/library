from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_author():
    response = client.post(
        "/authors/create",
        json=[{"name": "Tolstoy"}, {"name": "Pushkin"}],
    )
    assert response.status_code == 200
    r_json: dict = response.json()
    assert len(r_json) == 2
    for resp in r_json:
        assert "name", "id" in resp


def test_get_authors():
    response = client.get("/authors", params={"skip": 0, "limit": 3})
    assert response.status_code == 200
    r_json: dict = response.json()
    assert len(r_json) <= 3
    for resp in r_json:
        assert "name", "id" in resp


def test_get_author_by_id():
    response = client.get("/authors/7")
    assert response.status_code == 200
    r_json: dict = response.json()
    assert r_json["id"] == 7
    assert "name" in r_json


def test_delete_author():
    response = client.delete("/authors/7")
    assert response.status_code == 200
    assert response.json() == {"message": "Author with id=7 deleted"}
