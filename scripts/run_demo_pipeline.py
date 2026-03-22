from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.db.repositories.document_repository import DocumentRepository  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.services.parsers.service import extract_text_by_format  # noqa: E402
from app.services.pipeline import DocumentPipelineService  # noqa: E402
from app.utils.text import clean_text  # noqa: E402


def ensure_documents() -> list[int]:
    texts_dir = ROOT / "sample_data" / "texts"
    created_ids: list[int] = []

    with SessionLocal() as session:
        repository = DocumentRepository(session)
        existing = {document.filename: document.id for document in repository.list()}

        for path in sorted(texts_dir.iterdir()):
            if not path.is_file():
                continue

            document_id = existing.get(path.name)
            if document_id is None:
                document = repository.create(
                    filename=path.name,
                    format=path.suffix.lstrip("."),
                    source_type="demo_seed",
                    storage_path=str(path),
                    original_text=clean_text(
                        extract_text_by_format(path.suffix.lstrip("."), path.read_bytes())
                    ),
                    processing_status="uploaded",
                )
                session.commit()
                session.refresh(document)
                document_id = document.id
                print(f"Создан документ #{document_id}: {path.name}")
            created_ids.append(document_id)

    return created_ids


def main() -> None:
    document_ids = ensure_documents()

    with SessionLocal() as session:
        pipeline = DocumentPipelineService(session)
        for document_id in document_ids:
            result = pipeline.extract_document(document_id)
            print(
                f"Документ #{document_id}: статус={result.status}, чанков={result.chunks_created}, событий={result.events_created}"
            )


if __name__ == "__main__":
    main()
