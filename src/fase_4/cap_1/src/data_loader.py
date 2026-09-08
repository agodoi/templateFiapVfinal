"""
Utilities to load CSV data used by the Streamlit app.
"""

from pathlib import Path
import logging

import pandas as pd

from .database import (
    get_connection,
    compare_csv_with_tables,
    insert_sensores_iot_from_dataframe,
    create_sensores_iot_table,
)

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "sensores_data.csv"


def load_csv(path: Path | str | None = None) -> pd.DataFrame:
    """Load the primary sensors CSV."""
    csv_path = Path(path) if path else DEFAULT_CSV_PATH

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV não encontrado em: {csv_path}")

    return pd.read_csv(csv_path)


def ensure_table_and_upload(df: pd.DataFrame) -> int:
    """Ensure CS_SENSORES_IOT exists and upload DataFrame rows."""
    conn = get_connection()
    try:
        create_sensores_iot_table(conn)
        return insert_sensores_iot_from_dataframe(
            conn,
            df,
            allow_if_exists=False,
        )
    finally:
        conn.close()


def analyze_compatibility(df: pd.DataFrame) -> dict:
    """Compare CSV columns with Oracle tables."""
    conn = get_connection()
    try:
        return compare_csv_with_tables(df, conn)
    finally:
        conn.close()