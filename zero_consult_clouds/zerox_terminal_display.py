from __future__ import annotations

import os
import subprocess
from rich.console import Console
from rich.markdown import Markdown

# Reuse color codes from interactive_fill for consistent look
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLINK = "\033[5m"


def zerox_terminal_display(text: str) -> None:
    """Render ``text`` in a pager with light markdown support.

    The output is wrapped at 100 characters wide and shows navigation instructions.
    """

    console = Console(width=100, record=True)
    console.print(Markdown(text))
    body = console.export_text()

    header = f"""{BOLD}{CYAN}
==============================================================================
Move with j/k. g/G for start/end. / to search. n for next result. q to quit.
{GREEN}{BLINK}Press 'q' to continue.{RESET}{CYAN}
==============================================================================
{RESET}"""

    content = header + "\n" + body
    pager = os.environ.get("PAGER", "less -R")
    subprocess.run(pager, input=content.encode("utf-8"), shell=True)

__all__ = ["zerox_terminal_display"]
