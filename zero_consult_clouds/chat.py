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
        reply = response["choices"][0]["message"]["content"]
        self.history.append({"role": "assistant", "content": reply})
        return reply


__all__ = ["ChatGPT"]

