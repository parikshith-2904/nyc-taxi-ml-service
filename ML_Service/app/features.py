from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd


DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "taxi_zone_lookup.csv"
)


# Load valid NYC taxi zones once when the service starts
taxi_zones = pd.read_csv(DATA_PATH)

VALID_LOCATION_IDS = set(
    taxi_zones["LocationID"].astype(int)
)


def create_features(
    pickup_location_id: int,
    dropoff_location_id: int,
    pickup_datetime: str,
    passenger_count: float,
    rate_code: int,
) -> pd.DataFrame:

    # Validate pickup location
    if pickup_location_id not in VALID_LOCATION_IDS:
        raise ValueError(
            f"Invalid pickup location ID: {pickup_location_id}"
        )

    # Validate dropoff location
    if dropoff_location_id not in VALID_LOCATION_IDS:
        raise ValueError(
            f"Invalid dropoff location ID: {dropoff_location_id}"
        )

    # Convert datetime string to datetime object
    dt = datetime.fromisoformat(pickup_datetime)

    # Time features
    hour = dt.hour

    pickup_hour_sin = np.sin(
        2 * np.pi * hour / 24
    )

    pickup_hour_cos = np.cos(
        2 * np.pi * hour / 24
    )

    pickup_dayofweek = dt.weekday()

    # Create DataFrame using EXACT model feature names
    features = pd.DataFrame([{
        "PULocationID": pickup_location_id,
        "DOLocationID": dropoff_location_id,
        "passenger_count": passenger_count,
        "RatecodeID": rate_code,
        "pickup_hour_sin": pickup_hour_sin,
        "pickup_hour_cos": pickup_hour_cos,
        "pickup_dayofweek": pickup_dayofweek,
    }])

    return features