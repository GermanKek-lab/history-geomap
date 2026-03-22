from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.document import Document
from app.db.repositories.document_repository import DocumentRepository
from app.services.parsers.service import ALLOWED_FORMATS, extract_text_by_format
from app.utils.files import ensure_parent, normalize_filename
from app.utils.text import clean_text


class IngestService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.documents = DocumentRepository(session)

    def _ensure_filename_is_available(self, filename: str) -> None:
        if self.documents.exists_by_filename(filename):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Документ с именем {filename!r} уже существует. Используйте другое название файла.",
            )

    async def ingest(
        self,
        *,
        file: UploadFile | None = None,
        manual_text: str | None = None,
        manual_filename: str | None = None,
    ) -> Document:
        if file is not None:
            return await self._ingest_file(file)
        return self._ingest_manual_text(manual_text or "", manual_filename)

    async def _ingest_file(self, file: UploadFile) -> Document:
        filename = normalize_filename(file.filename or "document.txt")
        self._ensure_filename_is_available(filename)
        extension = Path(filename).suffix.lower().lstrip(".")
        if extension not in ALLOWED_FORMATS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Формат {extension!r} не поддерживается. Разрешено: {', '.join(sorted(ALLOWED_FORMATS))}.",
            )

        content = await file.read()
        if len(content) > settings.max_upload_size_mb * 1024 * 1024:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Файл слишком большой.")

        try:
            text = clean_text(extract_text_by_format(extension, content))
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка парсинга файла: {exc}") from exc

        if not text:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Из файла не удалось извлечь текст.")

        stored_path = settings.upload_dir / filename
        ensure_parent(stored_path)
        stored_path.write_bytes(content)

        document = self.documents.create(
            filename=filename,
            format=extension,
            source_type="file",
            storage_path=str(stored_path),
            original_text=text,
            processing_status="uploaded",
        )
        self.session.commit()
        self.session.refresh(document)
        return document

    def _ingest_manual_text(self, manual_text: str, manual_filename: str | None) -> Document:
        text = clean_text(manual_text)
        if not text:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пустой текст не может быть загружен.")

        filename = normalize_filename(manual_filename or "manual_input.txt")
        self._ensure_filename_is_available(filename)
        document = self.documents.create(
            filename=filename,
            format="txt",
            source_type="manual",
            storage_path=None,
            original_text=text,
            processing_status="uploaded",
        )
        self.session.commit()
        self.session.refresh(document)
        return document
