from fastapi.testclient import TestClient

from config import settings


def preflight(client: TestClient, origin: str):
    return client.options(
        "/auth/token",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )


def test_cors_allows_origin_from_allowlist(client: TestClient) -> None:
    allowed_origin = settings.allowed_origins[0]

    response = preflight(client, allowed_origin)

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == allowed_origin


def test_cors_rejects_origin_outside_allowlist(client: TestClient) -> None:
    response = preflight(client, "https://evil.example.com")

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_cors_allowlist_has_no_wildcard() -> None:
    assert "*" not in settings.allowed_origins
