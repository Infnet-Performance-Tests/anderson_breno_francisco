"""Modelos Pydantic de SAÍDA."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PredictionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    intent: str
    confidence: float
    created_at: datetime
