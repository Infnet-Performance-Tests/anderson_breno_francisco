"""(c) Envio de campo extra no body da request (extra='forbid') no /predict real."""

from models.prediction import PredictionRequest
from models.requests import StrictRequest


def test_campo_extra_no_body_e_rejeitado(client, admin_headers):
    resp = client.post(
        "/predict",
        json={"text": "I need help with a refund", "owner_id": 1, "is_admin": True},
        headers=admin_headers,
    )

    assert resp.status_code == 422
    rejeitados = {e["loc"][-1] for e in resp.json()["detail"] if e["type"] == "extra_forbidden"}
    assert {"owner_id", "is_admin"} <= rejeitados


def test_body_valido_continua_funcionando(client, admin_headers):
    """Controle positivo: sem campo extra, a request passa e o stub do TP1 segue igual."""
    resp = client.post(
        "/predict", json={"text": "I need help with a refund"}, headers=admin_headers
    )
    assert resp.status_code == 200
    assert resp.json()["intent"] == "general_inquiry"


def test_modelo_de_request_herda_da_base_estrita():
    assert issubclass(PredictionRequest, StrictRequest)
    assert PredictionRequest.model_config["extra"] == "forbid"
