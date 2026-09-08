from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

# Project root (two levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"

# Load .env from project root if present. This makes scripts work regardless
# of the current working directory used to invoke them.
load_dotenv(dotenv_path=ENV_PATH)


@dataclass(frozen=True)
class OracleConfig:
    user: str | None
    password: str | None
    dsn: str | None

    @property
    def is_configured(self) -> bool:
        return bool(self.user and self.password and self.dsn)


def get_oracle_config() -> OracleConfig:
    return OracleConfig(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN"),
    )