"""Utilities for appending git metadata to docs."""

from __future__ import annotations

from pathlib import Path
import subprocess


def _git(*args: str) -> str:
    result = subprocess.run(["git", *args], stdout=subprocess.PIPE, text=True, check=False)
    return result.stdout.strip()


def append_git_info(path: Path) -> None:
    """Append a section with git commit info to ``path``."""
    commit = _git("log", "-1", "--pretty=%H")
    with path.open("a", encoding="utf-8") as fh:
        fh.write("\n\n# Git Info\n")
        fh.write(f"Commit: {commit}\n")
