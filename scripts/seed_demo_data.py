from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.db.repositories.document_repository import DocumentRepository  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.services.pipeline import DocumentPipelineService  # noqa: E402
from app.services.parsers.service import extract_text_by_format  # noqa: E402
from app.utils.text import clean_text  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Загрузка демо-источников в GeoAutoMap.")
    parser.add_argument("--extract", action="store_true", help="Сразу запустить extraction pipeline для каждого документа.")
    args = parser.parse_args()

    texts_dir = ROOT / "sample_data" / "texts"
    sample_files = sorted(path for path in texts_dir.iterdir() if path.is_file())

    with SessionLocal() as session:
        documents = DocumentRepository(session)
        existing = {document.filename for document in documents.list()}
        pipeline = DocumentPipelineService(session)

        for path in sample_files:
            if path.name in existing:
                print(f"Пропуск: {path.name} уже есть в базе.")
                continue

            document = documents.create(
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
            print(f"Создан документ #{document.id}: {document.filename}")

            if args.extract:
                result = pipeline.extract_document(document.id)
                print(f"  -> pipeline: {result.events_created} событий, {result.chunks_created} чанков")


if __name__ == "__main__":
    main()
