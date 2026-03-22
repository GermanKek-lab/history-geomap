from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.db.models.text_chunk import TextChunk


class TextChunkRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def replace_for_document(self, document_id: int, chunks: Iterable[str]) -> list[TextChunk]:
        self.session.execute(delete(TextChunk).where(TextChunk.document_id == document_id))
        items: list[TextChunk] = []
        for index, chunk_text in enumerate(chunks):
            item = TextChunk(document_id=document_id, chunk_index=index, chunk_text=chunk_text)
            self.session.add(item)
            items.append(item)
        self.session.flush()
        return items
