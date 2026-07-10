from fastapi import APIRouter
import pandas as pd

from ..ml_model import model
from ..schemas import (
    PredictionRequest,
    PredictionResponse,
)

router = APIRouter(
    prefix="/predict",
    tags=["AI Prediction"]
)


@router.post(
    "/failure",
    response_model=PredictionResponse
)
def predict_failure(data: PredictionRequest):

    df = pd.DataFrame(
        [data.model_dump()]
    )

    prediction = model.predict(df)[0]

    probability = model.predict_proba(df)[0][1]

    if prediction == 1:
        result = "High Failure Risk"
    else:
        result = "Machine Healthy"

    return PredictionResponse(
        prediction=result,
        probability=round(
            probability * 100,
            2
        )
    )