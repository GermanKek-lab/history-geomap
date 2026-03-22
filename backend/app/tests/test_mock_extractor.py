from app.services.llm.mock_extractor import MockLLMExtractor


def test_mock_extractor_extracts_multiple_events_from_single_sentence() -> None:
    extractor = MockLLMExtractor()

    events = extractor.extract(
        "В 1812 году в Тарутино армия начала поход, а затем в Малоярославце произошло сражение."
    )

    assert len(events) == 2
    assert events[0].event_type == "march"
    assert events[0].place_name == "Тарутино"
    assert events[1].event_type == "battle"
    assert events[1].place_name == "Малоярославце"


def test_mock_extractor_extracts_continuation_event_from_next_sentence() -> None:
    extractor = MockLLMExtractor()

    events = extractor.extract(
        "В октябре 1812 года в Тарутино русская армия начала поход преследования после оставления Москвы. "
        "Позднее командование изменило направление марша и подготовило маневр к Малоярославцу."
    )

    assert len(events) == 2
    assert events[0].time_raw == "1812 года"
    assert events[0].place_name == "Тарутино"
    assert events[1].time_raw == "1812 года"
    assert events[1].place_name == "Малоярославцу"


def test_mock_extractor_prefers_specific_place_in_clause() -> None:
    extractor = MockLLMExtractor()

    events = extractor.extract(
        "7 сентября 1812 года у села Бородино, недалеко от Москвы, состоялось Бородинское сражение."
    )

    assert len(events) == 1
    assert events[0].place_name == "Бородино"


def test_mock_extractor_extracts_all_obvious_events_from_paragraph() -> None:
    extractor = MockLLMExtractor()

    events = extractor.extract(
        "7 сентября 1812 года под Бородино произошло сражение. "
        "19 октября 1812 года из Москвы началось отступление армии Наполеона. "
        "24 октября 1812 года в Малоярославце произошло новое сражение. "
        "В ноябре 1812 года под Вязьмой продолжилось отступление."
    )

    assert len(events) == 4
    assert [event.place_name for event in events] == ["Бородино", "Москвы", "Малоярославце", "Вязьмой"]
