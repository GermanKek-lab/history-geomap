from app.services.event_linking.linker import EventLinker


def test_event_linker_deduplicates_by_key_and_keeps_highest_confidence() -> None:
    linker = EventLinker()
    payload = [
        {
            "document_id": 1,
            "time_raw": "1812 года",
            "place_name_raw": "Тарутино",
            "place_name_normalized": "Тарутино",
            "event_type": "march",
            "action": "поход",
            "confidence": 0.65,
        },
        {
            "document_id": 1,
            "time_raw": "1812 года",
            "place_name_raw": "Тарутино",
            "place_name_normalized": "Тарутино",
            "event_type": "march",
            "action": "поход",
            "confidence": 0.82,
        },
    ]
    result = linker.deduplicate(payload)
    assert len(result) == 1
    assert result[0]["confidence"] == 0.82
