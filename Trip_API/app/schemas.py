from pydantic import BaseModel, Field


class TripRequest(BaseModel):
    pickup_location_id: int = Field(..., ge=1)
    dropoff_location_id: int = Field(..., ge=1)
    passenger_count: float = Field(..., gt=0)
    rate_code: int = Field(..., ge=1)


class TripResponse(BaseModel):
    predicted_duration_minutes: float
    predicted_total_amount: float