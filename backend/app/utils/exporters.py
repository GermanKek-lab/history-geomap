from __future__ import annotations

import csv
import io
import json

from app.core.config import settings
from app.db.models.document import Document
from app.db.models.event import Event


def event_to_dict(event: Event) -> dict[str, object]:
    return {
        "id": event.id,
        "document_id": event.document_id,
        "chunk_id": event.chunk_id,
        "time_raw": event.time_raw,
        "time_normalized_start": event.time_normalized_start.isoformat() if event.time_normalized_start else None,
        "time_normalized_end": event.time_normalized_end.isoformat() if event.time_normalized_end else None,
        "period_label": event.period_label,
        "place_name_raw": event.place_name_raw,
        "place_name_normalized": event.place_name_normalized,
        "latitude": event.latitude,
        "longitude": event.longitude,
        "event_type": event.event_type,
        "action": event.action,
        "description": event.description,
        "confidence": event.confidence,
        "source_fragment": event.source_fragment,
        "is_reviewed": event.is_reviewed,
        "reviewer_comment": event.reviewer_comment,
        "created_at": event.created_at.isoformat(),
        "updated_at": event.updated_at.isoformat(),
    }


def events_to_csv(events: list[Event]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "id",
            "document_id",
            "chunk_id",
            "time_raw",
            "time_normalized_start",
            "time_normalized_end",
            "period_label",
            "place_name_raw",
            "place_name_normalized",
            "latitude",
            "longitude",
            "event_type",
            "action",
            "description",
            "confidence",
            "source_fragment",
            "is_reviewed",
            "reviewer_comment",
            "created_at",
            "updated_at",
        ],
    )
    writer.writeheader()
    for event in events:
        writer.writerow(event_to_dict(event))
    return output.getvalue()


def events_to_geojson(events: list[Event]) -> dict[str, object]:
    features: list[dict[str, object]] = []
    for event in events:
        if event.latitude is None or event.longitude is None:
            continue
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [event.longitude, event.latitude]},
                "properties": event_to_dict(event),
            }
        )
    return {"type": "FeatureCollection", "features": features}


def write_document_exports(document: Document, events: list[Event]) -> dict[str, str]:
    settings.export_dir.mkdir(parents=True, exist_ok=True)
    csv_path = settings.export_dir / f"document_{document.id}_events.csv"
    json_path = settings.export_dir / f"document_{document.id}_events.json"
    geojson_path = settings.export_dir / f"document_{document.id}_events.geojson"

    csv_path.write_text(events_to_csv(events), encoding="utf-8")
    json_path.write_text(
        json.dumps({"document_id": document.id, "filename": document.filename, "events": [event_to_dict(event) for event in events]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    geojson_path.write_text(json.dumps(events_to_geojson(events), ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "csv_path": str(csv_path),
        "json_path": str(json_path),
        "geojson_path": str(geojson_path),
    }
