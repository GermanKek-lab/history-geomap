from __future__ import annotations

import logging
from typing import Any

import requests

from app.core.config import settings
from app.services.llm.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


class GeminiClient:
    def __init__(self) -> None:
        self.api_key = settings.gemini_api_key
        self.model = settings.gemini_model
        self.timeout = settings.gemini_timeout_sec

    @property
    def is_enabled(self) -> bool:
        return bool(self.api_key)

    def generate_events_payload(self, chunk: str) -> str:
        if not self.is_enabled:
            raise RuntimeError("Gemini API key не настроен.")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        response = requests.post(
            url,
            params={"key": self.api_key},
            timeout=self.timeout,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": SYSTEM_PROMPT},
                            {"text": USER_PROMPT_TEMPLATE.format(chunk=chunk)},
                        ],
                    }
                ],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 2048,
                },
            },
        )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        candidates = payload.get("candidates") or []
        if not candidates:
            raise RuntimeError("Gemini не вернул кандидатов.")

        parts = candidates[0].get("content", {}).get("parts", [])
        text_parts = [part.get("text", "") for part in parts if part.get("text")]
        if not text_parts:
            raise RuntimeError("Gemini вернул пустой ответ.")
        return "\n".join(text_parts)
