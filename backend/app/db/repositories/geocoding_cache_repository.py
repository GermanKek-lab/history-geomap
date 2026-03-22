from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.geocoding_cache import GeocodingCache


class GeocodingCacheRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_query(self, query: str) -> GeocodingCache | None:
        stmt = select(GeocodingCache).where(GeocodingCache.query == query)
        return self.session.scalars(stmt).first()

    def upsert(
        self,
        *,
        query: str,
        normalized_name: str,
        latitude: float,
        longitude: float,
        source: str,
        confidence: float,
    ) -> GeocodingCache:
        item = self.get_by_query(query)
        if item is None:
            item = GeocodingCache(query=query, normalized_name=normalized_name, latitude=latitude, longitude=longitude, source=source, confidence=confidence)
        else:
            item.normalized_name = normalized_name
            item.latitude = latitude
            item.longitude = longitude
            item.source = source
            item.confidence = confidence
        self.session.add(item)
        self.session.flush()
        return item
