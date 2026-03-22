from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.document import DocumentDetail
from app.services.ingest_service import IngestService
from app.services.query_service import QueryService

router = APIRouter()


@router.post(
    "/upload",
    response_model=DocumentDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Загрузить файл или текст",
)
async def upload_document(
    session: Annotated[Session, Depends(get_session)],
    file: UploadFile | None = File(default=None),
    manual_text: str | None = Form(default=None),
    manual_filename: str | None = Form(default=None),
) -> DocumentDetail:
    if file is None and not manual_text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нужно передать файл или текст.")

    document = await IngestService(session).ingest(file=file, manual_text=manual_text, manual_filename=manual_filename)
    document_detail = QueryService(session).get_document(document.id)
    if document_detail is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Документ создан, но не найден после сохранения.")
    return document_detail
