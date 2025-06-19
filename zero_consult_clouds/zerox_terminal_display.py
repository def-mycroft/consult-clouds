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

CHAT_BG_STYLE = "on grey11"


def terminal_display(text: str, *, scroll: bool = True, chatbot: bool = False) -> None:
    """Render ``text`` with light markdown support.

    Parameters
    ----------
    text:
        Content to display.
    scroll:
        If True, show in a pager with navigation instructions.
    chatbot:
        If True, apply a subtle background color to highlight chatbot output.
    """
    console = Console(width=80, record=scroll)
    style = CHAT_BG_STYLE if chatbot else ""
    console.print(Markdown(text), style=style)
    body = console.export_text()

    if scroll:
        header = f"""{BOLD}{CYAN}
==============================================================================
Move with j/k. g/G for start/end. / to search. n for next result. q to quit.
{GREEN}{BLINK}Press 'q' to continue.{RESET}{CYAN}
==============================================================================
{RESET}"""
        content = header + "\n" + body
        pager = os.environ.get("PAGER", "less -R")
        subprocess.run(pager, input=content.encode("utf-8"), shell=True)
    else:
        print(body)

# Backwards compatibility
zerox_terminal_display = terminal_display

__all__ = ["terminal_display", "zerox_terminal_display"]
