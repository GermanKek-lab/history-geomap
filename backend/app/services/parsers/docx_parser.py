from __future__ import annotations

from io import BytesIO

from docx import Document as DocxDocument


def parse_docx(content: bytes) -> str:
    document = DocxDocument(BytesIO(content))
    return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())
