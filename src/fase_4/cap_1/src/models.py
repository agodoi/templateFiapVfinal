"""
Training and evaluation utilities for regression models.

This module provides a clean Scikit-Learn pipeline for the FarmTech dashboard.
It trains regression models, evaluates them with MAE, MSE, RMSE and R², and
returns a PredictionResult dataclass used by the Streamlit pages.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .schemas import PredictionMetrics, PredictionResult


def _get_model(model_name: str):
    """Return a deterministic regression model by name."""
    models = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=8,
        ),
        "GradientBoosting": GradientBoostingRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=3,
        ),
    }

    return models.get(model_name, LinearRegression())


def _build_pipeline(model_name: str) -> Pipeline:
    """
    Build a Scikit-Learn pipeline.

    Tree-based models do not need scaling, but keeping the scaler makes the
    interface consistent and does not harm the demo.
    """
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", _get_model(model_name)),
        ]
    )


def train_and_evaluate(
    X: pd.DataFrame,
    y: pd.Series,
    model_name: str = "LinearRegression",
) -> PredictionResult:
    """
    Train a regression model and return predictions plus evaluation metrics.

    Parameters
    ----------
    X:
        Feature matrix.
    y:
        Numeric target vector.
    model_name:
        One of: LinearRegression, RandomForest, GradientBoosting.

    Returns
    -------
    PredictionResult
        Dataclass containing y_true, y_pred, metrics and model_name.
    """
    if X is None or y is None:
        raise ValueError("X e y não podem ser None.")

    if len(X) != len(y):
        raise ValueError("X e y precisam ter o mesmo número de linhas.")

    if len(X) < 5:
        raise ValueError("Dados insuficientes para treinar o modelo.")

    X = X.copy()
    y = pd.Series(y).copy()

    X = X.select_dtypes(include=[np.number])
    X = X.replace([np.inf, -np.inf], np.nan)
    y = y.replace([np.inf, -np.inf], np.nan)

    valid_index = X.dropna().index.intersection(y.dropna().index)
    X = X.loc[valid_index]
    y = y.loc[valid_index]

    if X.empty:
        raise ValueError("Nenhuma feature numérica válida foi encontrada.")

    if y.nunique() <= 1:
        raise ValueError("O target possui valor único. Não é possível treinar regressão.")

    test_size = 0.2 if len(X) >= 10 else 0.3

    x_train, x_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=42,
    )

    pipeline = _build_pipeline(model_name)
    pipeline.fit(x_train, y_train)

    y_pred = pipeline.predict(x_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = float(np.sqrt(mse))
    r2 = r2_score(y_test, y_pred)

    metrics = PredictionMetrics(
        mae=float(mae),
        mse=float(mse),
        rmse=rmse,
        r2=float(r2),
    )

    return PredictionResult(
        y_true=y_test.tolist(),
        y_pred=y_pred.tolist(),
        metrics=metrics,
        model_name=model_name,
    )