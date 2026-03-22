from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db.models.event import Event
    from app.db.models.text_chunk import TextChunk


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (UniqueConstraint("filename", name="uq_documents_filename"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    format: Mapped[str] = mapped_column(String(32), nullable=False)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False, default="file")
    storage_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    processing_status: Mapped[str] = mapped_column(String(32), nullable=False, default="uploaded")
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    chunks: Mapped[list["TextChunk"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="TextChunk.chunk_index",
    )
    events: Mapped[list["Event"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="Event.created_at",
    )
