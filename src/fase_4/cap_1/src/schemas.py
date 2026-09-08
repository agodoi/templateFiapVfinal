from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class PredictionMetrics:
    mae: float
    mse: float
    rmse: float
    r2: float

@dataclass
class PredictionResult:
    y_true: list
    y_pred: list
    metrics: PredictionMetrics
    model_name: str

@dataclass
class OracleConfig:
    user: str
    password: str
    dsn: str
