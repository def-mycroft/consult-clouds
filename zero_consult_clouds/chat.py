"""ChatGPT conversation helper."""
from __future__ import annotations

from pathlib import Path
import json
from os.path import join
from .helpers import prepend_obsidian_md, load_asset_template
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
        self.cfg = cfg
        if openai is None:
            raise RuntimeError("openai package not installed")
        openai.api_key = cfg.api_key
        self._model = cfg.model
        self.history: List[Dict[str, str]] = []
        self.last_response: Dict | None = None

    def update_transact_history(self, text_sent_to, text_gotten_back,
                                dict_full_history):
        """All Transactions (input/output pairs of text) Archived"""

        # TODO - codex: a small fix, apply this fix
        # codex: should have to setup a transaction_archive_filepath and use it
        # something like this below. need to set up this in setup-config
        # fp = self.cfg.transaction_archive_filepath

        fp = '/l/gds/consult-clouds-transactions.txt'

        date = pd.Timestamp.utcnow().tz_convert('America/Denver').isoformat()
        i = str(uuid())
        c = cdname(i)
        cx = c.split('-')[0]
        d = {'uuid':i, 'codename':c, 'date':date}
        templ_data = {'uuid':i, 'codename':c, 'date':date, 'search_name':cx,
                      'text_sent_to':text_sent_to,
                      'text_gotten_back':text_gotten_back}
        json_full_history = json.dumps(dict_full_history, indent=4)

        fp_json = join('/l/obs-chaotic', f"chat-hist-{i}.json")
        with open(fp_json, 'w') as f:
            f.write(json_full_history)
        templ_data['fp_full_history_json'] = fp_json

        with open(fp, 'a') as f:
            f.seek(0)
            f.write(f'\n# transaction {cx}\n')
            f.write(str(d))
            f.write(f"\n{'-'*100}\n")
            f.write(f'## sent there {cx}\n\n')
            f.write(text_sent_to)
            f.write(f"\n\n{'-'*100}\n")
            f.write(f'## gotten back {cx}\n\n')
            f.write(text_gotten_back)
            f.write(f"\n\n{'-'*100}\n")
            f.write('## full history {cx}\n\n')
            f.write(json_full_history)
            f.write(f"\n\n{'-'*100}\n")
        print(f"updated '{fp}'. archive id {c} {i}")

        # now update obs
        fn = f"cct {cx} {i.split('-')[0]} consult-clouds-transaction.md"
        fp = join('/l/obs-chaotic', fn)
        templ = load_asset_template('obsidian-promptlog.md.j2')
        with open(fp, 'w') as f:
            f.write(templ.render(templ_data))
        print(f"wrote '{fp}'")

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

        self.update_transact_history(prompt, reply, self.history)

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

