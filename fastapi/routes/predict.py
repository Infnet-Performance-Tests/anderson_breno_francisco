from fastapi import APIRouter

from application.prediction_facade import prediction_facade
from models.prediction import PredictionRequest, PredictionResponse
from security.dependencies import CurrentAdmin

router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
async def predict_intent(
    request: PredictionRequest,
    _current_admin: CurrentAdmin,
) -> PredictionResponse:
    prediction = prediction_facade.predict(request.text)
    return PredictionResponse(
        intent=prediction.intent,
        confidence=prediction.confidence,
        model_version=prediction.model_version,
    )
