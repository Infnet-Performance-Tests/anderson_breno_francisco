from domain.prediction import Intent, Prediction


class PredictionFacade:
    """Application boundary for intent prediction.

    The deterministic response is intentionally a stub. A later TP can replace
    this implementation without changing the HTTP contract.
    """

    def predict(self, text: str) -> Prediction:
        _ = text
        return Prediction(
            intent=Intent.GENERAL_INQUIRY,
            confidence=1.0,
            model_version="stub-v0",
        )


prediction_facade = PredictionFacade()
