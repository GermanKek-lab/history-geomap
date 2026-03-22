from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.geocoding import GeocodingResponse
from app.services.geocoding.service import GeocodingService

router = APIRouter()


@router.get("/geocoding/search", response_model=GeocodingResponse, summary="Проверка геокодинга топонима")
def geocoding_search(
    session: Annotated[Session, Depends(get_session)],
    q: str = Query(..., min_length=2, description="Топоним для поиска"),
) -> GeocodingResponse:
    result = GeocodingService(session).geocode(q)
    if result is None:
        raise HTTPException(status_code=404, detail="Координаты не найдены.")
    return GeocodingResponse.model_validate(result)
