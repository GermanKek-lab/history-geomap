from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[3]


def _default_upload_dir() -> Path:
    return ROOT_DIR / "data" / "uploads"


def _default_export_dir() -> Path:
    return ROOT_DIR / "sample_data" / "outputs"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    project_name: str = "GeoAutoMap"
    app_env: str = "development"
    debug: bool = False

    api_prefix: str = "/api"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    database_url: str = "postgresql+psycopg://geoautomap:geoautomap@localhost:5432/geoautomap"
    alembic_database_url: str = "postgresql+psycopg://geoautomap:geoautomap@localhost:5432/geoautomap"

    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://localhost:8080"]
    )

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"
    gemini_timeout_sec: int = 30
    llm_max_retries: int = 2
    enable_mock_llm: bool = True

    nominatim_enabled: bool = False
    nominatim_url: str = "https://nominatim.openstreetmap.org/search"

    max_upload_size_mb: int = 15
    chunk_size_chars: int = 1800
    chunk_overlap_chars: int = 200

    upload_dir: Path = Field(default_factory=_default_upload_dir)
    export_dir: Path = Field(default_factory=_default_export_dir)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        value = value.strip()
        if value.startswith("["):
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        return [item.strip() for item in value.split(",") if item.strip()]

    def prepare_directories(self) -> None:
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.export_dir.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    instance = Settings()
    instance.prepare_directories()
    return instance


settings = get_settings()
