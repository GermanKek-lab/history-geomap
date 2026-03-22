from __future__ import annotations

import logging
import re

from app.core.config import settings
from app.services.llm.gemini_client import GeminiClient
from app.services.llm.mock_extractor import MockLLMExtractor
from app.services.llm.validator import RawLLMEvent, parse_llm_events

logger = logging.getLogger(__name__)

SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")
WINDOW_MAX_CHARS = 720
WINDOW_MAX_SENTENCES = 3
WINDOW_OVERLAP_SENTENCES = 1


def _split_sentences(value: str) -> list[str]:
    return [sentence.strip() for sentence in re.split(SENTENCE_SPLIT_PATTERN, value) if sentence.strip()]


def _build_windows(chunk: str) -> list[str]:
    sentences = _split_sentences(chunk)
    if not sentences:
        return []
    if len(sentences) <= WINDOW_MAX_SENTENCES and len(chunk) <= WINDOW_MAX_CHARS:
        return [chunk]

    windows: list[str] = []
    start = 0
    while start < len(sentences):
        current: list[str] = []
        current_length = 0
        end = start

        while end < len(sentences):
            sentence = sentences[end]
            candidate_length = current_length + (1 if current else 0) + len(sentence)
            if current and (candidate_length > WINDOW_MAX_CHARS or len(current) >= WINDOW_MAX_SENTENCES):
                break
            current.append(sentence)
            current_length = candidate_length
            end += 1

        windows.append(" ".join(current))
        if end >= len(sentences):
            break
        start = max(start + 1, end - WINDOW_OVERLAP_SENTENCES)

    return windows


class LLMEventExtractor:
    def __init__(self) -> None:
        self.gemini = GeminiClient()
        self.mock = MockLLMExtractor()

    def _extract_with_gemini(self, chunk: str) -> list[RawLLMEvent]:
        for attempt in range(settings.llm_max_retries):
            try:
                raw = self.gemini.generate_events_payload(chunk)
                return parse_llm_events(raw)
            except Exception as exc:
                logger.warning("Gemini extraction attempt %s failed: %s", attempt + 1, exc)

        if not settings.enable_mock_llm:
            raise RuntimeError("Gemini недоступен и mock-режим отключен.")

        return self.mock.extract(chunk)

    def _deduplicate(self, events: list[RawLLMEvent]) -> list[RawLLMEvent]:
        unique: dict[tuple[str, str, str, str], RawLLMEvent] = {}
        for event in events:
            key = (
                event.time_raw.strip().lower(),
                event.place_name.strip().lower(),
                event.event_type.strip().lower(),
                event.action.strip().lower(),
            )
            current = unique.get(key)
            if current is None or event.confidence > current.confidence:
                unique[key] = event
        return list(unique.values())

    def extract(self, chunk: str) -> list[RawLLMEvent]:
        if not self.gemini.is_enabled:
            return self.mock.extract(chunk)

        events: list[RawLLMEvent] = []
        for window in _build_windows(chunk):
            events.extend(self._extract_with_gemini(window))

        merged = self._deduplicate(events)
        mock_events = self.mock.extract(chunk)
        if len(mock_events) > len(merged):
            merged = self._deduplicate([*merged, *mock_events])

        return merged
