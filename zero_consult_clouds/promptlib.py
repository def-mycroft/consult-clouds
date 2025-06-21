"""Utility functions for managing promptlib archives."""

from __future__ import annotations

from pathlib import Path


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


def browse(path: Path, filter_text: str = "") -> str | None:
    """Interactive prompt selector.

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

    values = []
    for fp in files:
        line = first_line(fp)
        label = f"{fp.name}\n    * {line}"
        values.append((str(fp), label))

    from prompt_toolkit.shortcuts import radiolist_dialog

    app = radiolist_dialog(
        title="promptlib browse",
        text=f"promptlib archive: {path}\ntotal: {len(files)} prompts",
        values=values,
        ok_text="select",
        cancel_text="quit",
    )
    return app.run()


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
