from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    pickup_location_id: int = Field(..., ge=1)
    dropoff_location_id: int = Field(..., ge=1)
    pickup_datetime: str
    passenger_count: float = Field(..., gt=0)
    rate_code: int = Field(..., ge=1)


class PredictionResponse(BaseModel):
    predicted_duration_minutes: float
    predicted_total_amount: float