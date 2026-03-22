from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.event import EventDetail, EventMapResponse, EventPatch, EventStatsResponse
from app.services.query_service import QueryService

router = APIRouter()


@router.get("/events", response_model=list[EventDetail], summary="Список событий с фильтрами")
def list_events(
    session: Annotated[Session, Depends(get_session)],
    document_id: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    event_type: str | None = None,
    min_confidence: float | None = Query(default=None, ge=0.0, le=1.0),
    place_query: str | None = None,
) -> list[EventDetail]:
    return QueryService(session).list_events(
        document_id=document_id,
        year_from=year_from,
        year_to=year_to,
        event_type=event_type,
        min_confidence=min_confidence,
        place_query=place_query,
    )


@router.get("/events/map", response_model=EventMapResponse, summary="GeoJSON для карты")
def map_events(
    session: Annotated[Session, Depends(get_session)],
    document_id: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    event_type: str | None = None,
    min_confidence: float | None = Query(default=None, ge=0.0, le=1.0),
    place_query: str | None = None,
) -> EventMapResponse:
    return QueryService(session).get_events_geojson(
        document_id=document_id,
        year_from=year_from,
        year_to=year_to,
        event_type=event_type,
        min_confidence=min_confidence,
        place_query=place_query,
    )


@router.get("/events/stats", response_model=EventStatsResponse, summary="Статистика по событиям")
def events_stats(session: Annotated[Session, Depends(get_session)]) -> EventStatsResponse:
    return QueryService(session).get_event_stats()


@router.get("/events/{event_id}", response_model=EventDetail, summary="Детальная карточка события")
def get_event(event_id: int, session: Annotated[Session, Depends(get_session)]) -> EventDetail:
    event = QueryService(session).get_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Событие не найдено.")
    return event


@router.patch("/events/{event_id}", response_model=EventDetail, summary="Ручное исправление события")
def patch_event(
    event_id: int,
    payload: EventPatch,
    session: Annotated[Session, Depends(get_session)],
) -> EventDetail:
    event = QueryService(session).update_event(event_id, payload)
    if event is None:
        raise HTTPException(status_code=404, detail="Событие не найдено.")
    return event
