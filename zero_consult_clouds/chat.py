"""ChatGPT conversation helper."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

try:  # pragma: no cover - openai optional
    import openai  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback
    openai = None  # type: ignore

from .config import CONFIG_FILE, Config, load_config


class ChatGPT:
    """Manage a single conversation with the OpenAI API."""

    def __init__(self, config_path: Path | None = None) -> None:
        cfg = load_config(config_path or CONFIG_FILE)
        if openai is None:
            raise RuntimeError("openai package not installed")
        openai.api_key = cfg.api_key
        self._model = cfg.default_model
        self.history: List[Dict[str, str]] = []
        self.last_response: Dict | None = None

    def send(
        self,
        prompt: str,
        *,
        model: str | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Send ``prompt`` and return the reply."""

        self.history.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=model or self._model,
            messages=self.history,
            max_tokens=max_tokens,
        )
        self.last_response = response
        reply = response["choices"][0]["message"]["content"]
        self.history.append({"role": "assistant", "content": reply})
        return reply


import re


def write_history(prompt: str, response: Dict, *, output_dir: Path) -> None:
    """Write or update ``history.md`` with ``prompt`` and ``response``."""

    out = output_dir / "history.md"
    if out.exists():
        text = out.read_text(encoding="utf-8")
    else:
        text = ""

    pattern = re.compile(
        r"^## Prompt (\d+)\n(.*?)\n### Response \1\n(.*?)\n---\n",
        re.DOTALL | re.MULTILINE,
    )
    entries = [
        (m.group(2).strip(), m.group(3).strip()) for m in pattern.finditer(text)
    ]
    entries.insert(0, (prompt, response["choices"][0]["message"]["content"]))

    lines = ["# Conversation History", "", "## Table of Contents"]
    for i in range(1, len(entries) + 1):
        lines.append(f"- [Prompt {i}](#prompt-{i})")
    lines.append("")

    for i, (p_text, r_text) in enumerate(entries, 1):
        lines.append(f"## Prompt {i}")
        lines.append(p_text)
        lines.append("")
        lines.append(f"### Response {i}")
        lines.append(r_text)
        lines.append("")
        lines.append("---")
        lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")


__all__ = ["ChatGPT", "write_history"]

