"""Public API for :mod:`zero_consult_clouds`."""

from .chat import ChatGPT
from .config import (
    CONFIG_FILE,
    Config,
    load_config,
    save_config,
    setup_config,
)
from . import cli, promptlib

__version__ = "0.1.0"

__all__ = [
    "ChatGPT",
    "CONFIG_FILE",
    "Config",
    "load_config",
    "save_config",
    "setup_config",
    "cli",
    "promptlib",
]
from .rewrite_loops import iterative_rewrite
from .chunking_processor import chunk_content, build_context_windows

__all__.append("iterative_rewrite")
__all__.extend(["chunk_content", "build_context_windows"])
