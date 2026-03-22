from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

import requests
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.repositories.geocoding_cache_repository import GeocodingCacheRepository
from app.services.geocoding.local_gazetteer import LOCAL_GAZETTEER

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class GeocodingResult:
    query: str
    normalized_name: str
    latitude: float
    longitude: float
    source: str
    confidence: float


class GeocodingService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.cache_repo = GeocodingCacheRepository(session)

    @staticmethod
    def normalize_query(query: str) -> str:
        normalized = re.sub(r"\s+", " ", query.strip().lower())
        normalized = normalized.strip(",.;:!? ")
        return normalized

    @staticmethod
    def _stem(query: str) -> str:
        for ending in ("ами", "ями", "ого", "ему", "ому", "ах", "ях", "ом", "ем", "ой", "ей"):
            if query.endswith(ending) and len(query) > len(ending) + 2:
                return query[: -len(ending)]
        if query.endswith(("а", "е", "у", "ы", "и", "о", "ю", "я")) and len(query) > 4:
            return query[:-1]
        return query

    def geocode(self, query: str) -> GeocodingResult | None:
        normalized_query = self.normalize_query(query)
        if not normalized_query:
            return None

        cached = self.cache_repo.get_by_query(normalized_query)
        if cached is not None:
            return GeocodingResult(
                query=query,
                normalized_name=cached.normalized_name,
                latitude=cached.latitude,
                longitude=cached.longitude,
                source=cached.source,
                confidence=cached.confidence,
            )

        local = self._search_local(normalized_query)
        if local is not None:
            self.cache_repo.upsert(
                query=normalized_query,
                normalized_name=local.normalized_name,
                latitude=local.latitude,
                longitude=local.longitude,
                source=local.source,
                confidence=local.confidence,
            )
            return local

        external = self._search_nominatim(normalized_query)
        if external is not None:
            self.cache_repo.upsert(
                query=normalized_query,
                normalized_name=external.normalized_name,
                latitude=external.latitude,
                longitude=external.longitude,
                source=external.source,
                confidence=external.confidence,
            )
            return external

        return None

    def _search_local(self, normalized_query: str) -> GeocodingResult | None:
        normalized_stem = self._stem(normalized_query)
        for item in LOCAL_GAZETTEER:
            alias_stems = {self._stem(alias) for alias in item["aliases"]}
            canonical = item["canonical"].lower()
            canonical_stem = self._stem(canonical)
            if (
                normalized_query == canonical
                or normalized_query in item["aliases"]
                or normalized_stem == canonical_stem
                or normalized_stem in alias_stems
            ):
                return GeocodingResult(
                    query=normalized_query,
                    normalized_name=item["canonical"],
                    latitude=item["latitude"],
                    longitude=item["longitude"],
                    source="local_gazetteer",
                    confidence=0.95,
                )

        for item in LOCAL_GAZETTEER:
            canonical = item["canonical"].lower()
            if normalized_query in canonical or normalized_stem in self._stem(canonical):
                return GeocodingResult(
                    query=normalized_query,
                    normalized_name=item["canonical"],
                    latitude=item["latitude"],
                    longitude=item["longitude"],
                    source="local_gazetteer_fuzzy",
                    confidence=0.72,
                )

        return None

    def _search_nominatim(self, normalized_query: str) -> GeocodingResult | None:
        if not settings.nominatim_enabled:
            return None

        try:
            response = requests.get(
                settings.nominatim_url,
                params={"q": normalized_query, "format": "jsonv2", "limit": 1},
                timeout=10,
                headers={"User-Agent": "GeoAutoMap/1.0"},
            )
            response.raise_for_status()
            payload: list[dict[str, Any]] = response.json()
        except Exception as exc:
            logger.warning("Nominatim request failed: %s", exc)
            return None

        if not payload:
            return None

        first = payload[0]
        return GeocodingResult(
            query=normalized_query,
            normalized_name=first.get("display_name", normalized_query),
            latitude=float(first["lat"]),
            longitude=float(first["lon"]),
            source="nominatim",
            confidence=0.65,
        )
