"""Modelos Pydantic de ENTRADA. Todos rejeitam campos extras (extra='forbid')."""
from pydantic import BaseModel, ConfigDict, Field


class StrictRequest(BaseModel):
    """Base de todos os bodies recebidos pela API."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class PredictRequest(StrictRequest):
    text: str = Field(min_length=1, max_length=2000)
