"""Fixtures dos testes da raiz (tests/).

- Usam o app REAL (fastapi/main.py) e um banco TEMPORÁRIO criado por sqlite_database.init_db(),
  então o fastapi/database.db versionado nunca é alterado.
- Tokens são session-scoped: o /auth/token terá rate limit de 10 req/min (SlowAPI).
- Os testes HTTP de ownership só rodam quando a rota GET /predictions/{prediction_id} existir
  e o login de alice/bob usar o banco (parte de autenticação/ownership do grupo).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "fastapi"))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import Session, create_engine  # noqa: E402

import sqlite_database  # noqa: E402
from database import get_session  # noqa: E402
from main import app  # noqa: E402

OWNERSHIP_ROUTE = "/predictions/{prediction_id}"


@pytest.fixture(scope="session")
def db_file(tmp_path_factory):
    path = tmp_path_factory.mktemp("db") / "test.db"
    sqlite_database.init_db(path)
    return path


@pytest.fixture
def session(db_file):
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    with Session(engine) as s:
        yield s


@pytest.fixture(scope="session")
def client(db_file):
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})

    def override_get_session():
        with Session(engine) as s:
            yield s

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _login(client, username, password):
    resp = client.post("/auth/token", data={"username": username, "password": password})
    if resp.status_code != 200:
        return None
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


@pytest.fixture(scope="session")
def admin_headers(client):
    headers = _login(client, "admin", "admin123")
    assert headers, "login do admin falhou"
    return headers


def _user_headers(client, username, password):
    if OWNERSHIP_ROUTE not in app.openapi()["paths"]:
        pytest.skip(f"rota GET {OWNERSHIP_ROUTE} ainda não existe no app")
    headers = _login(client, username, password)
    if headers is None:
        pytest.skip(f"login de {username} ainda não usa o banco de usuários")
    return headers


@pytest.fixture(scope="session")
def alice_headers(client):
    return _user_headers(client, "alice", "alice123")


@pytest.fixture(scope="session")
def bob_headers(client):
    return _user_headers(client, "bob", "bob123")
