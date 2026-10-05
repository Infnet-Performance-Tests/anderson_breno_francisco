"""Tabelas do banco (SQLModel)."""
from datetime import datetime, timezone

from pydantic import NaiveDatetime
from sqlmodel import Field, SQLModel


def _utcnow() -> NaiveDatetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = True


class Prediction(SQLModel, table=True):
    __tablename__ = "predictions"

    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="users.id", index=True)
    text: str
    intent: str
    confidence: float
    created_at: NaiveDatetime = Field(default_factory=_utcnow)
