from fastapi.testclient import TestClient

REQUIRED_HEADERS = {
    "strict-transport-security": "max-age=31536000; includeSubDomains",
    "x-frame-options": "DENY",
    "x-content-type-options": "nosniff",
    "content-security-policy": "default-src 'none'; frame-ancestors 'none'",
}


def test_security_headers_are_present_on_success_responses(client: TestClient) -> None:
    response = client.get("/health")

    for name, value in REQUIRED_HEADERS.items():
        assert response.headers[name] == value


def test_security_headers_are_present_on_error_responses(client: TestClient) -> None:
    response = client.post("/predict", json={"text": "I need a refund"})

    assert response.status_code == 401
    for name, value in REQUIRED_HEADERS.items():
        assert response.headers[name] == value


def test_swagger_ui_keeps_transport_headers_but_skips_csp(client: TestClient) -> None:
    response = client.get("/docs")

    assert response.status_code == 200
    assert response.headers["x-frame-options"] == "DENY"
    assert "content-security-policy" not in response.headers
