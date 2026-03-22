from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.schemas.common import ApiModel


class DocumentListItem(ApiModel):
    id: int
    filename: str
    format: str
    source_type: str
    processing_status: str
    last_error: str | None = None
    uploaded_at: datetime
    chunks_count: int = 0
    events_count: int = 0


class DocumentDetail(DocumentListItem):
    storage_path: str | None = None
    original_text: str


class DocumentTextResponse(ApiModel):
    id: int
    filename: str
    text: str


class ExtractionResponse(ApiModel):
    document_id: int
    status: str
    chunks_created: int
    events_created: int
    warnings: list[str] = Field(default_factory=list)
    csv_path: str | None = None
    json_path: str | None = None
    geojson_path: str | None = None


class DocumentExportResponse(ApiModel):
    document_id: int
    filename: str
    events: list[dict[str, object]]
