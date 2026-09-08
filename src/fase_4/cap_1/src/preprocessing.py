"""
Preprocessing helpers for feature engineering used by models and pages.

Keep the transformations deterministic and easily testable.
"""

import pandas as pd
from typing import Tuple


def derive_volume_irrigacao(df: pd.DataFrame) -> pd.DataFrame:
    """Add `volume_irrigacao_estimado` column using a simple heuristic.

    The heuristic is intentionally simple and interpretable — it is a
    composition of an inverse function of soil moisture, a temperature
    adjustment and an irrigation action multiplier.
    """
    df = df.copy()

    def compute(row):
        base = max(0, 60 - row.get('umidade_solo', 0)) * 0.8
        temp_adj = max(0, row.get('temperatura', 0) - 28) * 1.5
        acion = row.get('acao_irrigacao', 0) * 10
        return max(0.0, base + temp_adj + acion)

    df['volume_irrigacao_estimado'] = df.apply(compute, axis=1)
    return df


def prepare_features(df: pd.DataFrame, target: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Prepare feature matrix X and target vector y for modeling.

    Returns `(X, y)` and keeps the selection minimal for clarity.
    """
    df2 = derive_volume_irrigacao(df)
    X = df2[['temperatura', 'nutrientes_N', 'umidade_solo']].copy()
    y = df2[target].copy()
    return X, y
