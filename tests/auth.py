from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_login_for_access_token():
    response = client.get("/token")
    assert response.status_code == 200
    r_json: dict = response.json()
    assert r_json["token_type"] == "bearer"
    assert "access_token" in r_json
