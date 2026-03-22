from sqlalchemy.orm import Session

from app.services.geocoding.service import GeocodingService


def test_local_geocoding_exact_match() -> None:
    service = GeocodingService(Session())
    service.cache_repo.get_by_query = lambda query: None  # type: ignore[method-assign]
    service.cache_repo.upsert = lambda **kwargs: None  # type: ignore[method-assign]
    result = service.geocode("Бородино")
    assert result is not None
    assert result.normalized_name == "Бородино"
    assert result.source == "local_gazetteer"


def test_local_geocoding_handles_inflected_form() -> None:
    service = GeocodingService(Session())
    service.cache_repo.get_by_query = lambda query: None  # type: ignore[method-assign]
    service.cache_repo.upsert = lambda **kwargs: None  # type: ignore[method-assign]
    result = service.geocode("Севастополе")
    assert result is not None
    assert result.normalized_name == "Севастополь"
