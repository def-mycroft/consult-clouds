"""Utility functions for managing promptlib archives."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.shortcuts import CompleteStyle

__all__ = [
    "iter_prompt_files",
    "first_line",
    "browse",
    "cat",
    "stats",
]


def iter_prompt_files(path: Path, filter_text: str | None = None):
    """Yield promptlib files in ``path`` matching ``filter_text``."""
    for fp in sorted(path.glob("*promptlib*")):
        if filter_text and filter_text not in fp.name:
            continue
        if fp.is_file():
            yield fp


def first_line(path: Path) -> str:
    """Return the first non-empty line of ``path`` or an empty string."""
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                return line
    except Exception:
        pass
    return ""


def browse(
    path: Path,
    filter_text: str = "",
    output_file: Path | None = None,
) -> str | None:
    """Interactive prompt selector that appends to ``output_file``.

    Parameters
    ----------
    path:
        Directory containing promptlib files.
    filter_text:
        Optional substring filter for filenames.

    Returns
    -------
    str | None
        Selected file path or ``None`` if aborted.
    """
    files = list(iter_prompt_files(path, filter_text))
    if not files:
        print("no prompts found")
        return None

    print(f"promptlib archive: {path}")
    print(f"total: {len(files)} prompts")

    mapping: dict[str, Path] = {}
    display_items = []
    for i, fp in enumerate(files, 1):
        line = first_line(fp)
        display = f"{fp.name} - {line}"
        print(f"[{i}] {display}")
        mapping[str(i)] = fp
        mapping[display] = fp
        display_items.append(display)

    session = PromptSession()
    completer = FuzzyWordCompleter(display_items)

    while True:
        try:
            sel = session.prompt(
                "Select number or search text ('q' to quit): ",
                completer=completer,
                complete_in_thread=True,
                complete_while_typing=True,
                complete_style=CompleteStyle.MULTI_COLUMN,
            ).strip()
        except (EOFError, KeyboardInterrupt):
            return None

        if sel.lower() in {"q", "quit", ""}:
            return None

        if sel.isdigit() and sel in mapping:
            selected = mapping[sel]
            break

        if sel in mapping:
            selected = mapping[sel]
            break

        print("invalid selection")

    if output_file is None:
        output_file = Path("/l/obs-chaotic/prompt.md")

    ans = input(f"Append {selected} to {output_file}? [y/N] ").strip().lower()
    if ans not in {"y", "yes"}:
        return None

    try:
        text = Path(selected).read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover - unexpected
        print(f"error reading {selected}: {exc}")
        return None

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("a", encoding="utf-8") as fh:
        if fh.tell() > 0:
            fh.write("\n")
        fh.write(text)
    print(f"appended to '{output_file}'")
    return selected


def cat(path: Path, uuid: str) -> str:
    """Return prompt content matching ``uuid``."""
    matches = [p for p in path.glob(f"*{uuid}*promptlib*") if p.is_file()]
    if len(matches) != 1:
        raise RuntimeError(f"expected one match for {uuid}, found {len(matches)}")
    return matches[0].read_text(encoding="utf-8")


def stats(path: Path) -> tuple[int, Path]:
    """Return number of prompt files and archive path."""
    total = len(list(iter_prompt_files(path)))
    return total, path
