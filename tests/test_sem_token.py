"""(a) Tentativa de acesso sem token (opcional aqui: pode ser de outro integrante)."""


def test_acesso_sem_token_e_negado(client):
    assert client.post("/predict", json={"text": "hello"}).status_code == 401
    assert client.get("/predictions").status_code == 401
    assert client.get("/predictions/1").status_code == 401
