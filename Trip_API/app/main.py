import os
from datetime import datetime

import httpx
from fastapi import FastAPI, HTTPException

from .schemas import TripRequest, TripResponse


app = FastAPI(
    title="NYC Taxi Trip API",
    description="Public API for NYC taxi trip predictions.",
    version="1.0.0",
)

ML_SERVICE_URL = os.getenv(
    "ML_SERVICE_URL",
    "http://localhost:8001"
)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post(
    "/trips/predict",
    response_model=TripResponse
)
async def predict_trip(request: TripRequest):

    # Get the current date and time from the PC
    pickup_datetime = datetime.now().astimezone()

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{ML_SERVICE_URL}/predict",
                json={
                    "pickup_location_id": request.pickup_location_id,
                    "dropoff_location_id": request.dropoff_location_id,
                    "pickup_datetime": pickup_datetime.isoformat(),
                    "passenger_count": request.passenger_count,
                    "rate_code": request.rate_code,
                },
            )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="ML service is unavailable."
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="ML service returned an error."
        )

    prediction = response.json()

    return TripResponse(
        predicted_duration_minutes=prediction["predicted_duration_minutes"],
        predicted_total_amount=prediction["predicted_total_amount"],
    )