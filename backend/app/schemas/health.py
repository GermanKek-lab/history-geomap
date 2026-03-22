from __future__ import annotations

from app.schemas.common import ApiModel


class HealthResponse(ApiModel):
    status: str
    service: str
    environment: str
    database: bool
