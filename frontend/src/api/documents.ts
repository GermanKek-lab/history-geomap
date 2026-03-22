import type { DocumentDetail, DocumentItem, DocumentTextResponse, EventItem, ExtractionResponse } from "../types/api";
import { API_BASE_URL, request } from "./client";

export async function uploadDocument(payload: {
  file?: File | null;
  manualText?: string;
  manualFilename?: string;
}) {
  const form = new FormData();
  if (payload.file) {
    form.append("file", payload.file);
  }
  if (payload.manualText) {
    form.append("manual_text", payload.manualText);
  }
  if (payload.manualFilename) {
    form.append("manual_filename", payload.manualFilename);
  }
  return request<DocumentDetail>("/api/upload", {
    method: "POST",
    body: form,
  });
}

export function listDocuments() {
  return request<DocumentItem[]>("/api/documents");
}

export function getDocument(id: number) {
  return request<DocumentDetail>(`/api/documents/${id}`);
}

export function getDocumentText(id: number) {
  return request<DocumentTextResponse>(`/api/documents/${id}/text`);
}

export function extractDocument(id: number) {
  return request<ExtractionResponse>(`/api/documents/${id}/extract`, {
    method: "POST",
  });
}

export function getDocumentEvents(id: number) {
  return request<EventItem[]>(`/api/events?document_id=${id}`);
}

export function getCsvExportUrl(id: number) {
  return `${API_BASE_URL}/api/documents/${id}/export/csv`;
}

export function getJsonExportUrl(id: number) {
  return `${API_BASE_URL}/api/documents/${id}/export/json`;
}
