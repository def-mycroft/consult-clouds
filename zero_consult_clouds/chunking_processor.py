from __future__ import annotations

from pathlib import Path
from typing import List

from .config import CONFIG_FILE, load_config
from .helpers import count_tokens


_DEFAULT_RESERVE = 100


def chunk_content(text: str, *, config_path: Path = CONFIG_FILE, reserve: int = _DEFAULT_RESERVE) -> List[str]:
    """Break ``text`` into token-safe chunks using the configured model."""

    cfg = load_config(config_path)
    token_max = cfg.model_tokenmax or 16000
    limit = token_max - reserve
    words = text.split()
    chunks: List[str] = []
    current: List[str] = []
    for w in words:
        current.append(w)
        if count_tokens(" ".join(current), cfg.model) >= limit:
            if len(current) == 1:
                chunks.append(current[0])
                current = []
            else:
                current.pop()
                chunks.append(" ".join(current))
                current = [w]
    if current:
        chunks.append(" ".join(current))
    return chunks


def build_context_windows(chunks: List[str]) -> List[str]:
    """Return cumulative windows for ``chunks``."""

    windows: List[str] = []
    for i in range(len(chunks)):
        windows.append("\n".join(chunks[: i + 1]))
    return windows


__all__ = ["chunk_content", "build_context_windows"]
