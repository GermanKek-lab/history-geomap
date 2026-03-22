from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.db.repositories.document_repository import DocumentRepository
from app.db.repositories.event_repository import EventRepository
from app.db.repositories.text_chunk_repository import TextChunkRepository
from app.schemas.document import ExtractionResponse
from app.services.confidence.scorer import score_event_confidence
from app.services.datetime_normalization.normalizer import normalize_time_expression
from app.services.event_linking.linker import EventLinker
from app.services.geocoding.service import GeocodingService
from app.services.llm.extractor import LLMEventExtractor
from app.utils.exporters import write_document_exports
from app.utils.geo import make_point
from app.utils.text import chunk_text

logger = logging.getLogger(__name__)


class DocumentPipelineService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.documents = DocumentRepository(session)
        self.chunks = TextChunkRepository(session)
        self.events = EventRepository(session)
        self.extractor = LLMEventExtractor()
        self.geocoder = GeocodingService(session)
        self.linker = EventLinker()

    def extract_document(self, document_id: int) -> ExtractionResponse:
        document = self.documents.get(document_id)
        if document is None:
            raise ValueError("Документ не найден.")
        if not document.original_text.strip():
            raise ValueError("Документ не содержит текста.")

        warnings: list[str] = []

        try:
            self.documents.set_processing_state(document, "processing")
            self.session.commit()

            chunks = chunk_text(document.original_text)
            if not chunks:
                raise ValueError("После очистки текста не осталось содержимого для чанкинга.")

            stored_chunks = self.chunks.replace_for_document(document.id, chunks)

            prepared_events: list[dict[str, object]] = []
            for chunk in stored_chunks:
                raw_events = self.extractor.extract(chunk.chunk_text)
                for raw_event in raw_events:
                    normalized_date = normalize_time_expression(raw_event.time_raw)
                    geocoding_result = self.geocoder.geocode(raw_event.place_name)

                    if geocoding_result is None:
                        warnings.append(f"Не удалось геокодировать топоним: {raw_event.place_name}")

                    confidence = score_event_confidence(
                        raw_event.confidence,
                        geocoding_confidence=geocoding_result.confidence if geocoding_result else None,
                        date_precision=normalized_date.precision,
                    )

                    prepared_events.append(
                        {
                            "document_id": document.id,
                            "chunk_id": chunk.id,
                            "time_raw": raw_event.time_raw,
                            "time_normalized_start": normalized_date.start,
                            "time_normalized_end": normalized_date.end,
                            "period_label": raw_event.period or normalized_date.label,
                            "place_name_raw": raw_event.place_name,
                            "place_name_normalized": geocoding_result.normalized_name if geocoding_result else None,
                            "latitude": geocoding_result.latitude if geocoding_result else None,
                            "longitude": geocoding_result.longitude if geocoding_result else None,
                            "geom": make_point(
                                geocoding_result.latitude if geocoding_result else None,
                                geocoding_result.longitude if geocoding_result else None,
                            ),
                            "event_type": raw_event.event_type,
                            "action": raw_event.action,
                            "description": raw_event.description,
                            "confidence": confidence,
                            "source_fragment": raw_event.source_fragment,
                            "is_reviewed": False,
                            "reviewer_comment": None,
                        }
                    )

            linked_events = self.linker.deduplicate(prepared_events)
            created_events = self.events.replace_for_document(document.id, linked_events)
            self.documents.set_processing_state(document, "completed", None)

            self.session.commit()
            self.session.refresh(document)

            exports = write_document_exports(document, created_events)
            return ExtractionResponse(
                document_id=document.id,
                status=document.processing_status,
                chunks_created=len(stored_chunks),
                events_created=len(created_events),
                warnings=sorted(set(warnings)),
                **exports,
            )
        except Exception as exc:
            logger.exception("Pipeline failed for document %s", document_id)
            self.session.rollback()
            document = self.documents.get(document_id)
            if document is not None:
                self.documents.set_processing_state(document, "failed", str(exc))
                self.session.commit()
            raise
