"""(c) Envio de campo extra no body da request (extra='forbid')."""


def _total_predictions(client, headers):
    return len(client.get("/predictions", headers=headers).json())


def test_campo_extra_no_body_e_rejeitado(client, alice_headers):
    antes = _total_predictions(client, alice_headers)

    resp = client.post(
        "/predict",
        json={"text": "I need help with a refund", "owner_id": 1, "is_admin": True},
        headers=alice_headers,
    )

    assert resp.status_code == 422
    erros = resp.json()["detail"]
    campos_rejeitados = {e["loc"][-1] for e in erros if e["type"] == "extra_forbidden"}
    assert {"owner_id", "is_admin"} <= campos_rejeitados
    # Nada foi gravado no banco.
    assert _total_predictions(client, alice_headers) == antes


def test_body_valido_continua_funcionando(client, alice_headers):
    """Controle positivo: sem campo extra, a request passa."""
    resp = client.post("/predict", json={"text": "I need help with a refund"}, headers=alice_headers)
    assert resp.status_code == 200
    assert resp.json()["intent"]
