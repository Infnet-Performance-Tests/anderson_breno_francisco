from fastapi.testclient import TestClient

ATTEMPTS_ALLOWED_PER_MINUTE = 10


def failed_login(client: TestClient):
    return client.post("/auth/token", data={"username": "admin", "password": "wrong"})


def test_auth_token_returns_429_after_exceeding_limit(client: TestClient) -> None:
    for _ in range(ATTEMPTS_ALLOWED_PER_MINUTE):
        assert failed_login(client).status_code == 401

    response = failed_login(client)

    assert response.status_code == 429


def test_rate_limit_does_not_apply_to_other_endpoints(client: TestClient) -> None:
    for _ in range(ATTEMPTS_ALLOWED_PER_MINUTE + 1):
        failed_login(client)

    assert client.get("/health").status_code == 200
