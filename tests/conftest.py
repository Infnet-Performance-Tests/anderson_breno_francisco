"""Fixtures dos testes.

- Usa um banco TEMPORÁRIO criado pelo próprio sqlite_database.init_db(), então o
  fastapi/database.db real nunca é alterado pelos testes.
- Os tokens são session-scoped: o /auth/token tem rate limit de 10 req/min (SlowAPI),
  então fazemos só 2 logins em toda a suíte.
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


@pytest.fixture(scope="session")
def client(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("db") / "test.db"
    sqlite_database.init_db(db_file)
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})

    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _login(client, username, password):
    resp = client.post("/auth/token", data={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


@pytest.fixture(scope="session")
def alice_headers(client):
    return _login(client, "alice", "alice123")


@pytest.fixture(scope="session")
def bob_headers(client):
    return _login(client, "bob", "bob123")
