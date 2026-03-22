from __future__ import annotations

import markdown
from bs4 import BeautifulSoup


def parse_md(content: bytes) -> str:
    html = markdown.markdown(content.decode("utf-8", errors="ignore"))
    return BeautifulSoup(html, "html.parser").get_text("\n")
