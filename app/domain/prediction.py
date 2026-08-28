from dataclasses import dataclass
from enum import StrEnum


class Intent(StrEnum):
    GENERAL_INQUIRY = "general_inquiry"


@dataclass(frozen=True, slots=True)
class Prediction:
    intent: Intent
    confidence: float
    model_version: str
