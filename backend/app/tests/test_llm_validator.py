from app.services.llm.validator import parse_llm_events


def test_parse_llm_events_from_markdown_block() -> None:
    raw = """
    ```json
    [
      {
        "time_raw": "7 сентября 1812 года",
        "period": "Отечественная война 1812 года",
        "place_name": "Бородино",
        "event_type": "battle",
        "action": "сражение",
        "description": "Крупное сражение",
        "confidence": 0.87,
        "source_fragment": "..."
      }
    ]
    ```
    """
    events = parse_llm_events(raw)
    assert len(events) == 1
    assert events[0].event_type == "battle"
    assert events[0].place_name == "Бородино"
