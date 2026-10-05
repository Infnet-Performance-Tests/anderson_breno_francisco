"""Engine e dependência de sessão do SQLModel."""
import os
from pathlib import Path

from sqlmodel import Session, create_engine

DB_PATH = Path(os.getenv("DATABASE_PATH", Path(__file__).resolve().parent / "database.db"))

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session
