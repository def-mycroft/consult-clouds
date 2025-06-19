
try:
    from codenamize import codenamize as cd
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without the package
    def cd(value: str) -> str:
        """Simplistic fallback that returns the first eight characters."""
        return value[:8]
from uuid import uuid4 as uuid
from jinja2 import Environment, meta
import sys
import time
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


def extract_template_vars(template_or_str):
    """Extract undeclared Jinja2 variables as a dict.

    Parameters
    ----------
    template_or_str : str or jinja2.Template
        Template source string or loaded Template object.

    Returns
    -------
    dict
        Dictionary of variable names with value 0.
    """
    if hasattr(template_or_str, 'filename') and template_or_str.filename:
        path = Path(template_or_str.filename)
        template_str = path.read_text(encoding="utf-8")
    elif isinstance(template_or_str, str):
        template_str = template_or_str
    else:
        raise TypeError(f"Unsupported type for extract_template_vars: {type(template_or_str)}")

    env = Environment()
    parsed = env.parse(template_str)
    vars_found = meta.find_undeclared_variables(parsed)
    return {var.replace(' ', ''): 0 for var in vars_found}


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


import tiktoken


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Return the number of tokens ``text`` uses for ``model``."""

    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

