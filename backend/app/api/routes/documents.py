from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.document import DocumentDetail, DocumentExportResponse, DocumentListItem, DocumentTextResponse, ExtractionResponse
from app.services.pipeline import DocumentPipelineService
from app.services.query_service import QueryService

router = APIRouter()


@router.get("/documents", response_model=list[DocumentListItem], summary="Список документов")
def list_documents(session: Annotated[Session, Depends(get_session)]) -> list[DocumentListItem]:
    return QueryService(session).list_documents()


@router.get("/documents/{document_id}", response_model=DocumentDetail, summary="Карточка документа")
def get_document(document_id: int, session: Annotated[Session, Depends(get_session)]) -> DocumentDetail:
    document = QueryService(session).get_document(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Документ не найден.")
    return document


@router.get("/documents/{document_id}/text", response_model=DocumentTextResponse, summary="Исходный текст документа")
def get_document_text(document_id: int, session: Annotated[Session, Depends(get_session)]) -> DocumentTextResponse:
    document = QueryService(session).get_document(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Документ не найден.")
    return DocumentTextResponse(id=document.id, filename=document.filename, text=document.original_text)


@router.post("/documents/{document_id}/extract", response_model=ExtractionResponse, summary="Запуск extraction pipeline")
def extract_document(document_id: int, session: Annotated[Session, Depends(get_session)]) -> ExtractionResponse:
    service = DocumentPipelineService(session)
    try:
        return service.extract_document(document_id)
    except ValueError as exc:
        detail = str(exc)
        status_code = 404 if "не найден" in detail.lower() else 400
        raise HTTPException(status_code=status_code, detail=detail) from exc


@router.get("/documents/{document_id}/export/csv", summary="Экспорт событий документа в CSV")
def export_document_csv(document_id: int, session: Annotated[Session, Depends(get_session)]) -> Response:
    content = QueryService(session).export_document_csv(document_id)
    if content is None:
        raise HTTPException(status_code=404, detail="Документ не найден или для него нет событий.")
    return Response(
        content=content,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="document_{document_id}_events.csv"'},
    )


@router.get("/documents/{document_id}/export/json", response_model=DocumentExportResponse, summary="Экспорт событий документа в JSON")
def export_document_json(document_id: int, session: Annotated[Session, Depends(get_session)]) -> DocumentExportResponse:
    export = QueryService(session).export_document_json(document_id)
    if export is None:
        raise HTTPException(status_code=404, detail="Документ не найден.")
    return export
