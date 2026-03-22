from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ApiModel

EVENT_TYPES = [
    "battle",
    "march",
    "treaty",
    "political_event",
    "biography_event",
    "movement",
    "memoir_reference",
    "other",
]


class EventDetail(ApiModel):
    id: int
    document_id: int
    chunk_id: int | None = None
    time_raw: str
    time_normalized_start: date | None = None
    time_normalized_end: date | None = None
    period_label: str | None = None
    place_name_raw: str
    place_name_normalized: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    event_type: str
    action: str
    description: str
    confidence: float
    source_fragment: str
    is_reviewed: bool
    reviewer_comment: str | None = None
    created_at: datetime
    updated_at: datetime


class EventPatch(BaseModel):
    time_raw: str | None = None
    time_normalized_start: date | None = None
    time_normalized_end: date | None = None
    period_label: str | None = None
    place_name_raw: str | None = None
    place_name_normalized: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    event_type: str | None = None
    action: str | None = None
    description: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    source_fragment: str | None = None
    is_reviewed: bool | None = None
    reviewer_comment: str | None = None

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if value not in EVENT_TYPES:
            raise ValueError(f"Недопустимый тип события. Разрешено: {', '.join(EVENT_TYPES)}")
        return value


class GeoJsonFeature(ApiModel):
    type: str = "Feature"
    geometry: dict[str, object]
    properties: dict[str, object]


class EventMapResponse(ApiModel):
    type: str = "FeatureCollection"
    features: list[GeoJsonFeature]


class EventStatsBucket(ApiModel):
    label: str
    count: int


class EventStatsResponse(ApiModel):
    total_events: int
    reviewed_events: int
    without_coordinates: int
    by_type: list[EventStatsBucket]
    by_period: list[EventStatsBucket]
    by_year: list[EventStatsBucket]
