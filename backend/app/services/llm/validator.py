from __future__ import annotations

import json
import re
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.schemas.event import EVENT_TYPES


class RawLLMEvent(BaseModel):
    time_raw: str
    period: str | None = None
    place_name: str
    event_type: str
    action: str
    description: str
    confidence: float = Field(ge=0.0, le=1.0)
    source_fragment: str

    @field_validator("event_type")
    @classmethod
    def normalize_event_type(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in EVENT_TYPES:
            return "other"
        return normalized


def cleanup_json_like_text(raw: str) -> str:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    array_match = re.search(r"\[[\s\S]*\]", cleaned)
    if array_match:
        cleaned = array_match.group(0)

    cleaned = cleaned.replace("“", '"').replace("”", '"').replace("’", "'")
    cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)
    return cleaned


def parse_llm_events(raw: str) -> list[RawLLMEvent]:
    payload = cleanup_json_like_text(raw)
    parsed: Any = json.loads(payload)

    if isinstance(parsed, dict) and "events" in parsed:
        parsed = parsed["events"]

    if not isinstance(parsed, list):
        raise ValueError("LLM вернул не массив событий.")

    return [RawLLMEvent.model_validate(item) for item in parsed]
