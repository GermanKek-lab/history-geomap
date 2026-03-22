from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db.models.document import Document
    from app.db.models.text_chunk import TextChunk


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), index=True, nullable=False)
    chunk_id: Mapped[int | None] = mapped_column(ForeignKey("text_chunks.id", ondelete="SET NULL"), nullable=True)
    time_raw: Mapped[str] = mapped_column(String(255), nullable=False)
    time_normalized_start: Mapped[date | None] = mapped_column(Date, index=True, nullable=True)
    time_normalized_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    place_name_raw: Mapped[str] = mapped_column(String(255), nullable=False)
    place_name_normalized: Mapped[str | None] = mapped_column(String(255), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    geom: Mapped[str | None] = mapped_column(Geometry(geometry_type="POINT", srid=4326, spatial_index=True), nullable=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, index=True, nullable=False, default=0.0)
    source_fragment: Mapped[str] = mapped_column(Text, nullable=False)
    is_reviewed: Mapped[bool] = mapped_column(Boolean, index=True, nullable=False, default=False)
    reviewer_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    document: Mapped["Document"] = relationship(back_populates="events")
    chunk: Mapped["TextChunk | None"] = relationship(back_populates="events")
