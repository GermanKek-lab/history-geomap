from app.db.base import Base


def test_base_metadata_registers_all_models() -> None:
    assert "documents" in Base.metadata.tables
    assert "events" in Base.metadata.tables
    assert "text_chunks" in Base.metadata.tables
    assert "geocoding_cache" in Base.metadata.tables
