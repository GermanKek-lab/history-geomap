from __future__ import annotations

import re

from app.core.config import settings


def clean_text(value: str) -> str:
    value = value.replace("\r\n", "\n")
    value = re.sub(r"\n{3,}", "\n\n", value)
    value = re.sub(r"[ \t]{2,}", " ", value)
    return value.strip()


def chunk_text(value: str) -> list[str]:
    cleaned = clean_text(value)
    paragraphs = [paragraph.strip() for paragraph in cleaned.split("\n\n") if paragraph.strip()]
    if not paragraphs:
        return []

    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= settings.chunk_size_chars:
            current = candidate
            continue

        if current:
            chunks.append(current)
        if len(paragraph) <= settings.chunk_size_chars:
            current = paragraph
            continue

        start = 0
        while start < len(paragraph):
            end = start + settings.chunk_size_chars
            chunks.append(paragraph[start:end])
            start = end - settings.chunk_overlap_chars if settings.chunk_overlap_chars < settings.chunk_size_chars else end
        current = ""

    if current:
        chunks.append(current)
    return chunks
