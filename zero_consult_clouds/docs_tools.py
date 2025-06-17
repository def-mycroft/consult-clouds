"""Utilities for working with documentation.

This module centralizes helpers for interacting with the ``docs`` folder so
that they can easily be reused across projects with a similar layout.  The
functions only rely on :mod:`pathlib` and the ``helpers`` module shipped with
this package.
"""

from __future__ import annotations

from pathlib import Path
import re

from . import git_tools

from .helpers import codename, load_asset_template


_TEMPLATE_NAME = "new_doc_template.md.j2"

# default documentation directory relative to the package root
_DEFAULT_DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"


def _load_template() -> str:
    return load_asset_template(_TEMPLATE_NAME)


def new_doc(*, docs_dir: Path | None = None) -> Path:
    """Create a new documentation stub and return the path.

    Parameters
    ----------
    docs_dir:
        Optional target directory. Defaults to ``docs`` in the project root.

    """
    docs_dir = docs_dir or _DEFAULT_DOCS_DIR
    docs_dir.mkdir(parents=True, exist_ok=True)

    info = codename()
    code_str = f"{info['name']} {info['uuid'][:8]}"
    slug = f"unnamed-{info['name']}-{info['uuid'][:8]}".replace(" ", "-")

    tmpl = _load_template()
    if hasattr(tmpl, "render"):
        content = tmpl.render(codename=code_str)
    else:
        # simple string replacement fallback
        content = tmpl.replace("{{ codename }}", code_str)

    path = docs_dir / f"{slug}.md"
    path.write_text(content, encoding="utf-8")
    return path


def _title_from_file(path: Path) -> str:
    """Return the first non-empty line of ``path`` stripped of heading marks."""
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            return stripped.lstrip("#").strip()
    return ""


def _title_from_filename(name: str) -> str:
    base = Path(name).stem
    base = base.replace("_", " ").replace("-", " ")
    return base.title()


_PROMPT_RE = re.compile(r"^prompt[_-]?(\d+)")


def _tags_from_file(path: Path) -> set[str]:
    """Return a set of tag strings found in ``path``."""
    tags: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if re.fullmatch(r"#[A-Za-z0-9_-]+", stripped):
            tags.add(stripped)
    return tags


def _prompt_number(path: Path) -> int:
    """Return the integer prompt index extracted from ``path``."""
    match = _PROMPT_RE.match(path.stem)
    if match:
        return int(match.group(1))
    return -1


def generate_docs_toc(*, docs_dir: Path | None = None) -> str:
    """Generate a Markdown table of contents for Markdown files."""
    docs_dir = docs_dir or _DEFAULT_DOCS_DIR
    main_paths: list[Path] = []
    prompt_paths: list[Path] = []
    other_paths: list[Path] = []

    for path in sorted(docs_dir.glob("*.md")):
        name = path.name.lower()
        if name in {"readme.md", "contents.md"}:
            continue
        tags = _tags_from_file(path)
        if "#process-notes" in tags:
            main_paths.append(path)
        elif "#prompt" in tags:
            prompt_paths.append(path)
        else:
            other_paths.append(path)

    prompt_paths.sort(key=_prompt_number, reverse=True)

    lines = []
    lines.append("## Main Notes")
    if main_paths:
        for path in main_paths:
            title = _title_from_file(path)
            lines.append(f"- [{title}]({path.name})")
        lines.append("")
    else:
        lines.append(
            "- Place files named `main_notes*.md` in the docs folder to include them here."
        )
        lines.append("")
    if prompt_paths:
        lines.append("## Prompt Articles")
        for path in prompt_paths:
            title = _title_from_file(path)
            lines.append(f"- [{title}]({path.name})")
        lines.append("")

    lines.append("## Articles")
    for path in other_paths:
        title = _title_from_file(path)
        lines.append(f"- [{title}]({path.name})")

    return "\n".join(lines)


def update_toc(*, docs_dir: Path | None = None) -> None:
    """Write an auto-generated TOC to ``docs/CONTENTS.md``."""
    docs_dir = docs_dir or _DEFAULT_DOCS_DIR
    contents = docs_dir / "CONTENTS.md"
    toc = generate_docs_toc(docs_dir=docs_dir)
    with contents.open("w", encoding="utf-8") as fh:
        fh.write("# Table of Contents\n\n")
        fh.write(toc)
        fh.write("\n")


def analyze_docs(*, docs_dir: Path | None = None) -> None:
    """Append git commit info to all Markdown docs."""
    docs_dir = docs_dir or _DEFAULT_DOCS_DIR
    for path in sorted(docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "# Git Info" in text:
            continue
        git_tools.append_git_info(path)


__all__ = [
    "new_doc",
    "generate_docs_toc",
    "update_toc",
    "analyze_docs",
]

