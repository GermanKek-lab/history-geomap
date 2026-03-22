from __future__ import annotations

import re
from pathlib import Path


def normalize_filename(filename: str) -> str:
    safe = re.sub(r"[^a-zA-Zа-яА-Я0-9._-]+", "_", filename)
    return safe.strip("._") or "document.txt"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
