"""Simple interactive viewer for API responses.

The style mimics :mod:`interactive_fill` with mint green instructions and
light markdown rendering. Lines wrap at 100 characters.
"""

from __future__ import annotations

import os
import subprocess
from rich.console import Console
from rich.markdown import Markdown

# Reuse color codes from interactive_fill for visual consistency
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLINK = "\033[5m"


def interactive_view(text: str) -> None:
    """Display ``text`` in a pager with light Markdown rendering.

    The output uses ``less`` for navigation with basic Vim-style commands.
    Lines wrap at 100 columns.
    """

    console = Console(width=100, record=True)
    console.print(Markdown(text))
    body = console.export_text()

    header = f"""{BOLD}{CYAN}
===============================================================================
Move with j/k. g/G for start/end. / to search. n for next result. q to quit.
{GREEN}{BLINK}Press 'q' to continue.{RESET}{CYAN}
===============================================================================
{RESET}"""

    content = header + "\n" + body

    pager = os.environ.get("PAGER", "less -R")
    subprocess.run(pager, input=content.encode("utf-8"), shell=True)

