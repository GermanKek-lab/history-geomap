from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import date

from sqlalchemy import and_, delete, func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.db.models.event import Event


class EventRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def replace_for_document(self, document_id: int, events_payload: Iterable[dict[str, object]]) -> list[Event]:
        self.session.execute(delete(Event).where(Event.document_id == document_id))
        created: list[Event] = []
        for payload in events_payload:
            event = Event(**payload)
            self.session.add(event)
            created.append(event)
        self.session.flush()
        return created

    def get(self, event_id: int) -> Event | None:
        stmt = select(Event).options(joinedload(Event.document), joinedload(Event.chunk)).where(Event.id == event_id)
        return self.session.scalars(stmt).first()

    def list(
        self,
        *,
        document_id: int | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        event_type: str | None = None,
        min_confidence: float | None = None,
        place_query: str | None = None,
    ) -> Sequence[Event]:
        stmt = select(Event).options(joinedload(Event.document), joinedload(Event.chunk))

        if document_id is not None:
            stmt = stmt.where(Event.document_id == document_id)
        if year_from is not None:
            stmt = stmt.where(Event.time_normalized_start >= date(year_from, 1, 1))
        if year_to is not None:
            stmt = stmt.where(
                or_(
                    Event.time_normalized_end <= date(year_to, 12, 31),
                    and_(
                        Event.time_normalized_end.is_(None),
                        Event.time_normalized_start <= date(year_to, 12, 31),
                    ),
                    Event.time_normalized_start.is_(None),
                )
            )
        if event_type:
            stmt = stmt.where(Event.event_type == event_type)
        if min_confidence is not None:
            stmt = stmt.where(Event.confidence >= min_confidence)
        if place_query:
            pattern = f"%{place_query.lower()}%"
            stmt = stmt.where(
                or_(
                    func.lower(Event.place_name_raw).like(pattern),
                    func.lower(func.coalesce(Event.place_name_normalized, "")).like(pattern),
                )
            )

        return self.session.scalars(stmt.order_by(Event.time_normalized_start.asc().nullslast(), Event.created_at.desc())).all()

    def update(self, event: Event, **payload: object) -> Event:
        for field, value in payload.items():
            setattr(event, field, value)
        self.session.add(event)
        self.session.flush()
        return event
