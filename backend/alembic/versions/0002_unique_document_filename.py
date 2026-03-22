"""Add unique constraint for document filename."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0002_unique_document_filename"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    duplicates = bind.execute(
        sa.text(
            """
            SELECT filename
            FROM documents
            GROUP BY filename
            HAVING COUNT(*) > 1
            """
        )
    ).fetchall()

    if duplicates:
        names = ", ".join(row[0] for row in duplicates)
        raise RuntimeError(f"Невозможно добавить уникальность filename: найдены дубликаты ({names}).")

    op.create_unique_constraint("uq_documents_filename", "documents", ["filename"])


def downgrade() -> None:
    op.drop_constraint("uq_documents_filename", "documents", type_="unique")
