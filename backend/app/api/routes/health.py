from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="Проверка состояния сервиса")
def healthcheck() -> HealthResponse:
    database_ok = False

    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
            database_ok = True
    except Exception:
        database_ok = False

    return HealthResponse(
        status="ok",
        service=settings.project_name,
        environment=settings.app_env,
        database=database_ok,
    )
