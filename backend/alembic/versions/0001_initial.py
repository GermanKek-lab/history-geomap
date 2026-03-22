"""Initial schema for GeoAutoMap."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    if bind.dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("format", sa.String(length=32), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False, server_default="file"),
        sa.Column("storage_path", sa.String(length=512), nullable=True),
        sa.Column("original_text", sa.Text(), nullable=False),
        sa.Column("processing_status", sa.String(length=32), nullable=False, server_default="uploaded"),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_documents_uploaded_at", "documents", ["uploaded_at"])
    op.create_index("ix_documents_processing_status", "documents", ["processing_status"])

    op.create_table(
        "text_chunks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("document_id", sa.Integer(), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("chunk_text", sa.Text(), nullable=False),
        sa.UniqueConstraint("document_id", "chunk_index", name="uq_text_chunks_document_index"),
    )
    op.create_index("ix_text_chunks_document_id", "text_chunks", ["document_id"])

    op.create_table(
        "geocoding_cache",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("query", sa.String(length=255), nullable=False),
        sa.Column("normalized_name", sa.String(length=255), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.0"),
        sa.UniqueConstraint("query", name="uq_geocoding_cache_query"),
    )
    op.create_index("ix_geocoding_cache_normalized_name", "geocoding_cache", ["normalized_name"])

    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("document_id", sa.Integer(), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chunk_id", sa.Integer(), sa.ForeignKey("text_chunks.id", ondelete="SET NULL"), nullable=True),
        sa.Column("time_raw", sa.String(length=255), nullable=False),
        sa.Column("time_normalized_start", sa.Date(), nullable=True),
        sa.Column("time_normalized_end", sa.Date(), nullable=True),
        sa.Column("period_label", sa.String(length=255), nullable=True),
        sa.Column("place_name_raw", sa.String(length=255), nullable=False),
        sa.Column("place_name_normalized", sa.String(length=255), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("geom", Geometry(geometry_type="POINT", srid=4326, spatial_index=True), nullable=True),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("source_fragment", sa.Text(), nullable=False),
        sa.Column("is_reviewed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("reviewer_comment", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_events_document_id", "events", ["document_id"])
    op.create_index("ix_events_event_type", "events", ["event_type"])
    op.create_index("ix_events_time_normalized_start", "events", ["time_normalized_start"])
    op.create_index("ix_events_confidence", "events", ["confidence"])
    op.create_index("ix_events_is_reviewed", "events", ["is_reviewed"])

    if bind.dialect.name == "postgresql":
        op.execute("CREATE INDEX IF NOT EXISTS ix_events_geom ON events USING GIST (geom)")


def downgrade() -> None:
    bind = op.get_bind()

    if bind.dialect.name == "postgresql":
        op.execute("DROP INDEX IF EXISTS ix_events_geom")

    op.drop_index("ix_events_is_reviewed", table_name="events")
    op.drop_index("ix_events_confidence", table_name="events")
    op.drop_index("ix_events_time_normalized_start", table_name="events")
    op.drop_index("ix_events_event_type", table_name="events")
    op.drop_index("ix_events_document_id", table_name="events")
    op.drop_table("events")

    op.drop_index("ix_geocoding_cache_normalized_name", table_name="geocoding_cache")
    op.drop_table("geocoding_cache")

    op.drop_index("ix_text_chunks_document_id", table_name="text_chunks")
    op.drop_table("text_chunks")

    op.drop_index("ix_documents_processing_status", table_name="documents")
    op.drop_index("ix_documents_uploaded_at", table_name="documents")
    op.drop_table("documents")
