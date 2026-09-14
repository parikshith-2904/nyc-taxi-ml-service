from fastapi import FastAPI, HTTPException

from .schemas import (
    PredictionRequest,
    PredictionResponse,
)

from .features import create_features
from .models import predict


app = FastAPI(
    title="NYC Taxi ML Service",
    description="ML inference service for NYC taxi predictions.",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict_trip(request: PredictionRequest):

    try:

        features = create_features(
            pickup_location_id=request.pickup_location_id,
            dropoff_location_id=request.dropoff_location_id,
            pickup_datetime=request.pickup_datetime,
            passenger_count=request.passenger_count,
            rate_code=request.rate_code,
        )

        prediction = predict(features)

        return PredictionResponse(
            predicted_duration_minutes=prediction[
                "predicted_duration_minutes"
            ],
            predicted_total_amount=prediction[
                "predicted_total_amount"
            ],
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )