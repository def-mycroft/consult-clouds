"""Configuration utilities for :mod:`zero_consult_clouds`."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

try:  # pragma: no cover - yaml optional
    import yaml
except ModuleNotFoundError:  # pragma: no cover - simple JSON fallback
    import json as _json

    class _Y:
        @staticmethod
        def safe_load(s: str):
            return _json.loads(s)

        @staticmethod
        def safe_dump(d: Dict[str, Any]):
            return _json.dumps(d, indent=2)

    yaml = _Y()


CONFIG_DIR = Path.home() / ".config" / "zero_consult_clouds"
CONFIG_FILE = CONFIG_DIR / "config.yaml"


@dataclass
class Config:
    """Simple configuration container."""

    api_key: str
    default_model: str = "gpt-3.5-turbo"


def load_config(path: Path = CONFIG_FILE) -> Config:
    """Load configuration from ``path``.

    Parameters
    ----------
    path:
        YAML file to read.
    """

    if not path.exists():
        raise FileNotFoundError(str(path))

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if "api_key" not in data:
        raise KeyError("api_key missing in config")
    if "default_model" not in data:
        data["default_model"] = "gpt-3.5-turbo"
    return Config(**data)


def _atomic_write(text: str, path: Path) -> None:
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        fh.write(text)
    tmp.replace(path)


def save_config(cfg: Config, path: Path = CONFIG_FILE) -> None:
    """Write ``cfg`` to ``path`` atomically."""

    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write(yaml.safe_dump(cfg.__dict__), path)


def setup_config(
    *,
    path: Path = CONFIG_FILE,
    api_key: str | None = None,
    default_model: str = "gpt-3.5-turbo",
    interactive: bool = True,
) -> Config:
    """Interactively create or update configuration."""

    if interactive:
        if api_key is None:
            api_key = input("OpenAI API key: ").strip()
        model = input(f"Default model [{default_model}]: ").strip()
        if model:
            default_model = model
    else:
        if api_key is None:
            raise ValueError(
                "api_key required when interactive is False"
            )

    cfg = Config(api_key=api_key, default_model=default_model)
    save_config(cfg, path)
    return cfg


__all__ = [
    "Config",
    "load_config",
    "save_config",
    "setup_config",
    "CONFIG_FILE",
]

