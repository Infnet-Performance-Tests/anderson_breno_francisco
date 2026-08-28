from fastapi.testclient import TestClient


def test_auth_returns_bearer_token(client: TestClient) -> None:
    response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "admin123"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_auth_rejects_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "wrong"},
    )

    assert response.status_code == 401
