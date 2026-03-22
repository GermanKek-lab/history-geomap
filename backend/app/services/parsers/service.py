from __future__ import annotations

from collections.abc import Callable

from app.services.parsers.docx_parser import parse_docx
from app.services.parsers.html_parser import parse_html
from app.services.parsers.md_parser import parse_md
from app.services.parsers.pdf_parser import parse_pdf
from app.services.parsers.txt_parser import parse_txt

PARSERS: dict[str, Callable[[bytes], str]] = {
    "txt": parse_txt,
    "docx": parse_docx,
    "md": parse_md,
    "html": parse_html,
    "pdf": parse_pdf,
}

ALLOWED_FORMATS = set(PARSERS)


def extract_text_by_format(file_format: str, content: bytes) -> str:
    parser = PARSERS.get(file_format.lower())
    if parser is None:
        raise ValueError(f"Формат {file_format!r} не поддерживается.")
    return parser(content)
