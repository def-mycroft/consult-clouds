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
    model: str = "gpt-3.5-turbo"
    model_tokenmax: int | None = None
    default_output_dir: str | None = None
    promptlib_dir: str | None = None


def _default_tokenmax(model: str) -> int:
    if model == "gpt-4o":
        return 128000
    return 16000


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
    if "model" not in data and "default_model" in data:
        data["model"] = data.pop("default_model")
    if "model" not in data:
        data["model"] = "gpt-3.5-turbo"
    if "model-tokenmax" in data:
        data["model_tokenmax"] = data.pop("model-tokenmax")
    if "model_tokenmax" not in data:
        data["model_tokenmax"] = _default_tokenmax(data["model"])
    if "default_output_dir" not in data:
        data["default_output_dir"] = None
    if "promptlib_dir" not in data:
        data["promptlib_dir"] = None
    return Config(**data)


def _atomic_write(text: str, path: Path) -> None:
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        fh.write(text)
    tmp.replace(path)


def save_config(cfg: Config, path: Path = CONFIG_FILE) -> None:
    """Write ``cfg`` to ``path`` atomically."""

    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "api_key": cfg.api_key,
        "model": cfg.model,
        "model-tokenmax": cfg.model_tokenmax,
        "default_output_dir": cfg.default_output_dir,
        "promptlib_dir": cfg.promptlib_dir,
    }
    _atomic_write(yaml.safe_dump(data), path)
    print(f"wrote config '{path}'")


def setup_config(
    *,
    path: Path = CONFIG_FILE,
    api_key: str | None = None,
    model: str = "gpt-3.5-turbo",
    default_output_dir: str | None = None,
    promptlib_dir: str | None = None,
    interactive: bool = True,
) -> Config:
    """Interactively create or update configuration."""

    if interactive:
        if api_key is None:
            api_key = input("OpenAI API key: ").strip()
        mod_inp = input(f"Model [{model}]: ").strip()
        if mod_inp:
            model = mod_inp
        out_dir_inp = input(
            f"Default output dir [{default_output_dir or ''}]: "
        ).strip()
        if out_dir_inp:
            default_output_dir = out_dir_inp
        promptlib_inp = input(
            f"Promptlib dir [{promptlib_dir or ''}]: "
        ).strip()
        if promptlib_inp:
            promptlib_dir = promptlib_inp
    else:
        if api_key is None:
            raise ValueError(
                "api_key required when interactive is False"
            )

    cfg = Config(
        api_key=api_key,
        model=model,
        model_tokenmax=_default_tokenmax(model),
        default_output_dir=default_output_dir,
        promptlib_dir=promptlib_dir,
    )
    save_config(cfg, path)
    return cfg


__all__ = [
    "Config",
    "load_config",
    "save_config",
    "setup_config",
    "CONFIG_FILE",
]

