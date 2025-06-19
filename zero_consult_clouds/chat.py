"""ChatGPT conversation helper."""

from __future__ import annotations

from pathlib import Path
from .helpers import prepend_obsidian_md
import re
import pandas as pd
from uuid import uuid4 as uuid
from codenamize import codenamize as cdname
from typing import Dict, List
from jinja2 import Template

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
        self._model = cfg.model
        self.history: List[Dict[str, str]] = []
        self.last_response: Dict | None = None

    def append_to_global_log(self, prompt, reply):
        """A global log of all chats is updated"""
        # TODO - this needs to be integrated into config, i.e. fp_global_log
        # codex: this is something you could just do, if it is simple enough and
        # mention it as an aside in the commit. 
        fp_global_log = '/l/chatlog-consult-clouds.md'
        ########################################################################

        with open(fp_global_log, 'r') as f:
            text = f.read()
        dt = pd.Timestamp.utcnow().tz_convert('America/Denver')
        pattern = r"```jinja2\s*(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        templ = Template(matches[0])
        i = str(uuid())
        c = cdname(i)
        d = {'date':dt.isoformat(), 'uuid':i, 'codename':c,
             'uuid_prefix':i.split('-')[0], 'prompt':prompt, 'reply':reply}
        prepend_obsidian_md(fp_global_log, text=templ.render(d))

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
        self.append_to_global_log(prompt, reply)
        return reply




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

