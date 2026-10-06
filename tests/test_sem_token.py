"""(a) Tentativa de acesso sem token."""


def test_predict_sem_token_e_negado(client):
    assert client.post("/predict", json={"text": "hello"}).status_code == 401


def test_predict_com_token_invalido_e_negado(client):
    resp = client.post(
        "/predict", json={"text": "hello"}, headers={"Authorization": "Bearer token.invalido"}
    )
    assert resp.status_code == 401
