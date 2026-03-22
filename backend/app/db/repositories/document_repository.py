from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, selectinload

from app.db.models.document import Document


class DocumentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, **payload: object) -> Document:
        document = Document(**payload)
        self.session.add(document)
        self.session.flush()
        return document

    def get(self, document_id: int) -> Document | None:
        stmt: Select[tuple[Document]] = (
            select(Document)
            .options(selectinload(Document.chunks), selectinload(Document.events))
            .where(Document.id == document_id)
        )
        return self.session.scalars(stmt).first()

    def list(self) -> Sequence[Document]:
        stmt = select(Document).options(selectinload(Document.chunks), selectinload(Document.events)).order_by(Document.uploaded_at.desc())
        return self.session.scalars(stmt).all()

    def exists_by_filename(self, filename: str) -> bool:
        stmt = select(Document.id).where(func.lower(Document.filename) == filename.lower())
        return self.session.execute(stmt).first() is not None

    def set_processing_state(self, document: Document, status: str, error: str | None = None) -> Document:
        document.processing_status = status
        document.last_error = error
        self.session.add(document)
        self.session.flush()
        return document
