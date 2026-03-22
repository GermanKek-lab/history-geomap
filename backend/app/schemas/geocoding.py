from __future__ import annotations

from app.schemas.common import ApiModel


class GeocodingResponse(ApiModel):
    query: str
    normalized_name: str
    latitude: float
    longitude: float
    source: str
    confidence: float
