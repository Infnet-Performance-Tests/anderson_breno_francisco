"""Criação e população inicial do banco SQLite (usa sqlite3 puro, conforme o enunciado).

Uso (a partir da pasta fastapi/):
    python sqlite_database.py            # cria e popula se ainda estiver vazio
    python sqlite_database.py --reset    # apaga o database.db e recria do zero
"""
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

from security.passwords import hash_password

DB_PATH = Path(__file__).resolve().parent / "database.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL REFERENCES users (id),
    text VARCHAR NOT NULL,
    intent VARCHAR NOT NULL,
    confidence FLOAT NOT NULL,
    created_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_predictions_owner_id ON predictions (owner_id);
"""

# Credenciais acadêmicas (apenas para o trabalho).
SEED_USERS = [
    ("admin", "admin123"),  # usuário do TP1, mantido
    ("alice", "alice123"),
    ("bob", "bob123"),
]

# (username do dono, texto, intenção, confiança)
SEED_PREDICTIONS = [
    ("alice", "I need a refund for my last order", "refund_request", 0.91),
    ("alice", "My invoice has a wrong amount", "billing_inquiry", 0.84),
    ("bob", "The app crashes when I log in", "technical_issue", 0.88),
    ("bob", "How do I cancel my subscription?", "cancellation_request", 0.79),
    ("admin", "Where is my package?", "delivery_status", 0.82),
]


def _now() -> str:
    # Formato aceito pelo SQLAlchemy/SQLModel para colunas DateTime no SQLite.
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")


def init_db(db_path: Path | str = DB_PATH, reset: bool = False) -> Path:
    db_path = Path(db_path)
    if reset and db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SCHEMA)

        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
                [(u, hash_password(p)) for u, p in SEED_USERS],
            )
            ids = {u: i for i, u in conn.execute("SELECT id, username FROM users")}
            conn.executemany(
                "INSERT INTO predictions (owner_id, text, intent, confidence, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                [(ids[o], t, i, c, _now()) for o, t, i, c in SEED_PREDICTIONS],
            )
        conn.commit()
    finally:
        conn.close()
    return db_path


if __name__ == "__main__":
    path = init_db(reset="--reset" in sys.argv)
    with sqlite3.connect(path) as c:
        n_u = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        n_p = c.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
    print(f"Banco pronto em {path} ({n_u} usuários, {n_p} predictions)")
