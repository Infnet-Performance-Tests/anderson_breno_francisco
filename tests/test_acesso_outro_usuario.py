"""(b) Tentativa de acesso a recurso pertencente a outro usuário (BOLA).

Parte 1: camada de dados (sempre roda) - a consulta com ownership não devolve recurso alheio.
Parte 2: camada HTTP (roda quando a rota GET /predictions/{id} e o login via banco existirem).
"""

from sqlmodel import select

import crud
from models.tables import Prediction, User


def _user(session, username):
    return session.exec(select(User).where(User.username == username)).one()


# ---------- camada de dados ----------
def test_consulta_com_ownership_nao_retorna_recurso_de_outro_usuario(session):
    alice, bob = _user(session, "alice"), _user(session, "bob")
    alice_prediction = crud.list_predictions_by_owner(session, alice.id)[0]

    assert crud.get_prediction_for_owner(session, alice_prediction.id, alice.id) is not None
    assert crud.get_prediction_for_owner(session, alice_prediction.id, bob.id) is None


def test_listagem_por_dono_nao_mistura_usuarios(session):
    alice, bob = _user(session, "alice"), _user(session, "bob")
    alice_ids = {p.id for p in crud.list_predictions_by_owner(session, alice.id)}
    bob_ids = {p.id for p in crud.list_predictions_by_owner(session, bob.id)}

    assert alice_ids and bob_ids
    assert alice_ids.isdisjoint(bob_ids)
    assert all(
        p.owner_id == alice.id
        for p in session.exec(select(Prediction).where(Prediction.id.in_(alice_ids)))
    )


# ---------- camada HTTP ----------
def test_usuario_nao_acessa_prediction_de_outro_usuario(client, alice_headers, bob_headers):
    alice_prediction = client.get("/predictions", headers=alice_headers).json()[0]

    own = client.get(f"/predictions/{alice_prediction['id']}", headers=alice_headers)
    assert own.status_code == 200  # controle positivo: o dono acessa

    other = client.get(f"/predictions/{alice_prediction['id']}", headers=bob_headers)
    assert other.status_code in (403, 404)
    assert alice_prediction["text"] not in other.text


def test_id_de_outro_usuario_e_id_inexistente_tem_mesma_resposta(
    client, alice_headers, bob_headers
):
    """Não deve ser possível enumerar quais ids existem."""
    alice_id = client.get("/predictions", headers=alice_headers).json()[0]["id"]
    de_outro = client.get(f"/predictions/{alice_id}", headers=bob_headers)
    inexistente = client.get("/predictions/999999", headers=bob_headers)
    assert de_outro.status_code == inexistente.status_code
    assert de_outro.json() == inexistente.json()
