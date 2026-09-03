from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from domain.prediction import Intent

TicketText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=5_000),
]


class PredictionRequest(BaseModel):
    text: TicketText


class PredictionResponse(BaseModel):
    intent: Intent
    confidence: float = Field(ge=0.0, le=1.0)
    model_version: str
