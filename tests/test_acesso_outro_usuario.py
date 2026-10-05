"""(b) Tentativa de acesso a recurso pertencente a outro usuário (BOLA)."""


def test_usuario_nao_acessa_prediction_de_outro_usuario(client, alice_headers, bob_headers):
    # Alice lista as próprias predictions e pega o id de uma delas.
    resp = client.get("/predictions", headers=alice_headers)
    assert resp.status_code == 200
    alice_predictions = resp.json()
    assert alice_predictions, "o seed deveria ter predictions da alice"
    alice_prediction = alice_predictions[0]

    # Controle positivo: o dono consegue acessar.
    own = client.get(f"/predictions/{alice_prediction['id']}", headers=alice_headers)
    assert own.status_code == 200
    assert own.json()["text"] == alice_prediction["text"]

    # Bob tenta acessar o recurso da Alice: a API não pode retornar o recurso.
    other = client.get(f"/predictions/{alice_prediction['id']}", headers=bob_headers)
    assert other.status_code in (403, 404)
    assert alice_prediction["text"] not in other.text


def test_listagem_retorna_somente_predictions_do_dono(client, alice_headers, bob_headers):
    alice_ids = {p["id"] for p in client.get("/predictions", headers=alice_headers).json()}
    bob_ids = {p["id"] for p in client.get("/predictions", headers=bob_headers).json()}
    assert alice_ids and bob_ids
    assert alice_ids.isdisjoint(bob_ids)


def test_id_inexistente_e_id_de_outro_usuario_tem_mesma_resposta(
    client, alice_headers, bob_headers
):
    """Não deve ser possível descobrir (enumerar) quais ids existem."""
    alice_id = client.get("/predictions", headers=alice_headers).json()[0]["id"]
    de_outro = client.get(f"/predictions/{alice_id}", headers=bob_headers)
    inexistente = client.get("/predictions/999999", headers=bob_headers)
    assert de_outro.status_code == inexistente.status_code
    assert de_outro.json() == inexistente.json()
