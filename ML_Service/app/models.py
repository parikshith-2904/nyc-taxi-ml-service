from pathlib import Path

import joblib


MODEL_DIR = (
    Path(__file__).resolve().parent.parent
    / "models"
)


duration_model = joblib.load(
    MODEL_DIR / "duration_model.joblib"
)

fare_model = joblib.load(
    MODEL_DIR / "fare_model.joblib"
)


def predict(features):

    duration_prediction = duration_model.predict(features)[0]

    fare_prediction = fare_model.predict(features)[0]

    return {
        "predicted_duration_minutes": float(
            duration_prediction
        ),
        "predicted_total_amount": float(
            fare_prediction
        ),
    }