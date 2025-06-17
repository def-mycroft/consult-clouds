
try:
    from codenamize import codenamize as cd
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without the package
    def cd(value: str) -> str:
        """Simplistic fallback that returns the first eight characters."""
        return value[:8]
from uuid import uuid4 as uuid
from pathlib import Path
try:  # Optional dependency
    import pandas as pd  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback if pandas missing
    pd = None  # type: ignore
import inspect

from typing import Any, Callable, Dict

try:
    from jinja2 import Environment, FileSystemLoader
except ModuleNotFoundError:  # pragma: no cover - fallback if jinja2 missing
    Environment = None
    FileSystemLoader = None


def codename():
    """Generate random codename"""
    i = str(uuid())
    return {'uuid':i, 'name':cd(i)}


def load_asset_template(name: str):
    """Load a jinja2 template bundled in ``assets``.

    Parameters
    ----------
    name:
        File name of the template to load.
    """

    assets = Path(__file__).resolve().parent / "assets"
    if Environment is None:
        # jinja2 missing, fall back to plain text
        path = assets / name
        return path.read_text(encoding="utf-8")

    env = Environment(loader=FileSystemLoader(str(assets)))
    template = env.get_template(name)
    return template

