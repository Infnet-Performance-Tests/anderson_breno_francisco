from fastapi.testclient import TestClient


def test_predict_requires_authentication(client: TestClient) -> None:
    response = client.post("/predict", json={"text": "I need a refund"})

    assert response.status_code == 401


def test_predict_returns_stub_intent(client: TestClient, admin_token: str) -> None:
    response = client.post(
        "/predict",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"text": "I need a refund"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "intent": "general_inquiry",
        "confidence": 1.0,
        "model_version": "stub-v0",
    }


def test_predict_rejects_blank_text(client: TestClient, admin_token: str) -> None:
    response = client.post(
        "/predict",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"text": "   "},
    )

    assert response.status_code == 422
