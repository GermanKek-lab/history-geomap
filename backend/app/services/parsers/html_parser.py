from __future__ import annotations

from bs4 import BeautifulSoup


def parse_html(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")
    return soup.get_text("\n")
