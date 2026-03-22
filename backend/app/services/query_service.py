from __future__ import annotations

from collections import Counter

from sqlalchemy.orm import Session

from app.db.repositories.document_repository import DocumentRepository
from app.db.repositories.event_repository import EventRepository
from app.schemas.document import DocumentDetail, DocumentExportResponse, DocumentListItem
from app.schemas.event import EventDetail, EventMapResponse, EventPatch, EventStatsBucket, EventStatsResponse, GeoJsonFeature
from app.utils.exporters import event_to_dict, events_to_csv
from app.utils.geo import make_point


class QueryService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.documents = DocumentRepository(session)
        self.events = EventRepository(session)

    def list_documents(self) -> list[DocumentListItem]:
        result: list[DocumentListItem] = []
        for document in self.documents.list():
            result.append(
                DocumentListItem(
                    id=document.id,
                    filename=document.filename,
                    format=document.format,
                    source_type=document.source_type,
                    processing_status=document.processing_status,
                    last_error=document.last_error,
                    uploaded_at=document.uploaded_at,
                    chunks_count=len(document.chunks),
                    events_count=len(document.events),
                )
            )
        return result

    def get_document(self, document_id: int) -> DocumentDetail | None:
        document = self.documents.get(document_id)
        if document is None:
            return None
        return DocumentDetail(
            id=document.id,
            filename=document.filename,
            format=document.format,
            source_type=document.source_type,
            storage_path=document.storage_path,
            processing_status=document.processing_status,
            last_error=document.last_error,
            uploaded_at=document.uploaded_at,
            chunks_count=len(document.chunks),
            events_count=len(document.events),
            original_text=document.original_text,
        )

    def list_events(self, **filters: object) -> list[EventDetail]:
        items = self.events.list(**filters)
        return [EventDetail.model_validate(event, from_attributes=True) for event in items]

    def get_event(self, event_id: int) -> EventDetail | None:
        event = self.events.get(event_id)
        if event is None:
            return None
        return EventDetail.model_validate(event, from_attributes=True)

    def update_event(self, event_id: int, payload: EventPatch) -> EventDetail | None:
        event = self.events.get(event_id)
        if event is None:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        if "latitude" in update_data or "longitude" in update_data:
            latitude = update_data.get("latitude", event.latitude)
            longitude = update_data.get("longitude", event.longitude)
            update_data["geom"] = make_point(latitude, longitude)

        updated = self.events.update(event, **update_data)
        self.session.commit()
        self.session.refresh(updated)
        return EventDetail.model_validate(updated, from_attributes=True)

    def get_events_geojson(self, **filters: object) -> EventMapResponse:
        items = self.events.list(**filters)
        features: list[GeoJsonFeature] = []
        for event in items:
            if event.latitude is None or event.longitude is None:
                continue
            features.append(
                GeoJsonFeature(
                    geometry={"type": "Point", "coordinates": [event.longitude, event.latitude]},
                    properties=event_to_dict(event),
                )
            )
        return EventMapResponse(features=features)

    def export_document_csv(self, document_id: int) -> str | None:
        document = self.documents.get(document_id)
        if document is None:
            return None
        if not document.events:
            return None
        return events_to_csv(document.events)

    def export_document_json(self, document_id: int) -> DocumentExportResponse | None:
        document = self.documents.get(document_id)
        if document is None:
            return None
        return DocumentExportResponse(
            document_id=document.id,
            filename=document.filename,
            events=[event_to_dict(event) for event in document.events],
        )

    def get_event_stats(self) -> EventStatsResponse:
        items = list(self.events.list())
        by_type = Counter(event.event_type for event in items)
        by_period = Counter((event.period_label or "Без периода") for event in items)
        by_year = Counter(
            str(event.time_normalized_start.year) if event.time_normalized_start else "Не определен"
            for event in items
        )

        return EventStatsResponse(
            total_events=len(items),
            reviewed_events=sum(1 for event in items if event.is_reviewed),
            without_coordinates=sum(1 for event in items if event.latitude is None or event.longitude is None),
            by_type=[EventStatsBucket(label=label, count=count) for label, count in by_type.most_common()],
            by_period=[EventStatsBucket(label=label, count=count) for label, count in by_period.most_common(10)],
            by_year=[EventStatsBucket(label=label, count=count) for label, count in by_year.most_common(10)],
        )
