# NYC Taxi Trip Prediction API

An end-to-end machine learning system for predicting **NYC taxi trip duration and fare** using XGBoost, FastAPI, Docker, and a two-service architecture.

The project takes basic trip information such as pickup/drop-off locations, passenger count, and rate code, automatically generates time-based features, and returns predictions for:

- Trip duration in minutes
- Total fare amount excluding tip

---

## Architecture

```text
                         Client / Postman
                               │
                               │ POST /trips/predict
                               ▼
                    ┌─────────────────────┐
                    │      Trip API       │
                    │      FastAPI        │
                    │                     │
                    │ • Request validation│
                    │ • Generate current  │
                    │   pickup datetime   │
                    │ • Public API        │
                    └──────────┬──────────┘
                               │
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │     ML Service      │
                    │      FastAPI        │
                    │                     │
                    │ • Location validation
                    │ • Feature engineering
                    │ • Duration model   │
                    │ • Fare model       │
                    └──────────┬──────────┘
                               │
                         ┌─────┴─────┐
                         ▼           ▼
                   Duration      Fare Model
                   XGBoost        XGBoost
```
