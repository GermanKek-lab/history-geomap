from __future__ import annotations

import re
from collections import OrderedDict

from app.services.llm.validator import RawLLMEvent

EVENT_KEYWORDS = {
    "battle": ("битв", "сражен", "бой", "штурм", "столкновен", "атак", "контратак"),
    "march": ("поход", "марш", "отступлен", "двину", "переш", "наступлен", "маневр", "преследован"),
    "treaty": ("договор", "мир", "соглашен", "трактат"),
    "political_event": ("коронац", "восстан", "революц", "манифест"),
    "biography_event": ("родил", "умер", "назнач", "прибыл", "возглав", "отрек"),
    "movement": ("переселен", "движен", "эвакуац", "перемещ", "переброс"),
    "memoir_reference": ("вспоминал", "мемуар", "писал", "дневник", "свидетельств"),
}

TIME_PATTERNS = [
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b\d{1,2}\s+[а-яё]+\s+\d{4}\s+года\b",
    r"\b(?:в начале|в середине|в конце)\s+\d{4}\s+года\b",
    r"\b(?:в начале|в середине|в конце)\s+\d{4}\s+году\b",
    r"\b(?:в начале|в середине|в конце)\s+[XVI]+?\s+века\b",
    r"\b(?:весной|летом|осенью|зимой)\s+\d{4}\s+года\b",
    r"\b(?:весной|летом|осенью|зимой)\s+\d{4}\s+году\b",
    r"\b\d{4}\s+года\b",
    r"\b\d{4}\s+году\b",
]

PLACE_HINT_PATTERN = re.compile(
    r"\b(?:в|под|у|из|к|на|от|около|возле|между)\s+"
    r"(?:(?:городе?|селе|села|деревне|деревня|крепости|станции|поселке|хуторе)\s+)?"
    r"([А-ЯЁ][а-яё-]+(?:\s+[А-ЯЁ][а-яё-]+)?)"
)
SEGMENT_SPLIT_PATTERN = re.compile(
    r"(?:;\s+)|(?:,\s+(?=(?:а|но|и\s+затем|затем|после\s+этого|после\s+чего|позднее|позже|вскоре|далее)\b))"
)
CONTINUATION_PATTERN = re.compile(
    r"^(?:а\s+|и\s+)?(?:затем|после\s+этого|после\s+чего|позднее|позже|вскоре|далее|при\s+этом)\b",
    flags=re.IGNORECASE,
)
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")


def _detect_event_types(sentence: str) -> list[str]:
    lower = sentence.lower()
    return [event_type for event_type, keywords in EVENT_KEYWORDS.items() if any(keyword in lower for keyword in keywords)]


def _detect_time(sentence: str) -> str | None:
    for pattern in TIME_PATTERNS:
        match = re.search(pattern, sentence, flags=re.IGNORECASE)
        if match:
            return match.group(0)
    return None


def _detect_places(sentence: str) -> list[str]:
    matches = OrderedDict()
    for match in PLACE_HINT_PATTERN.finditer(sentence):
        candidate = match.group(1).strip(" ,.;:()[]{}\"'")
        if candidate:
            matches.setdefault(candidate, None)
    return list(matches)


def _split_segments(sentence: str) -> list[str]:
    segments = [segment.strip(" ,;:") for segment in re.split(SEGMENT_SPLIT_PATTERN, sentence) if segment.strip(" ,;:")]
    return segments or [sentence.strip()]


def _is_continuation(segment: str) -> bool:
    return bool(CONTINUATION_PATTERN.match(segment.strip()))


def _confidence_for_event_type(event_type: str) -> float:
    if event_type == "battle":
        return 0.86
    if event_type == "march":
        return 0.78
    if event_type == "memoir_reference":
        return 0.73
    return 0.62


class MockLLMExtractor:
    def extract(self, chunk: str) -> list[RawLLMEvent]:
        events: list[RawLLMEvent] = []
        sentences = [sentence.strip() for sentence in re.split(SENTENCE_SPLIT_PATTERN, chunk) if sentence.strip()]
        last_explicit_time: str | None = None
        last_explicit_place: str | None = None

        for sentence in sentences:
            sentence_time = _detect_time(sentence)
            sentence_places = _detect_places(sentence)
            sentence_place = sentence_places[0] if sentence_places else None
            sentence_event_emitted = False
            last_event_time: str | None = None
            last_event_place: str | None = None

            for segment in _split_segments(sentence):
                event_types = _detect_event_types(segment)
                if not event_types:
                    continue

                segment_time = _detect_time(segment)
                segment_places = _detect_places(segment)

                time_raw = segment_time or sentence_time
                place_name = segment_places[0] if segment_places else None

                if place_name is None and sentence_place and len(sentence_places) == 1:
                    place_name = sentence_place

                if time_raw is None and not segment_time:
                    time_raw = last_explicit_time

                if place_name is None and not segment_places:
                    if _is_continuation(segment) or sentence_event_emitted or not sentence_places:
                        place_name = last_explicit_place or sentence_place

                if not time_raw or not place_name:
                    continue

                for event_type in event_types:
                    events.append(
                        RawLLMEvent(
                            time_raw=time_raw,
                            period=None,
                            place_name=place_name,
                            event_type=event_type,
                            action=segment[:100],
                            description=segment[:240],
                            confidence=_confidence_for_event_type(event_type),
                            source_fragment=sentence[:400],
                        )
                    )
                    sentence_event_emitted = True
                    last_event_time = time_raw
                    last_event_place = place_name

            if sentence_time:
                last_explicit_time = sentence_time
            elif sentence_event_emitted and last_event_time:
                last_explicit_time = last_event_time

            if sentence_place:
                last_explicit_place = sentence_place
            elif sentence_event_emitted and last_event_place:
                last_explicit_place = last_event_place

        return events
