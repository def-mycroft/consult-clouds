"""Simple interactive viewer for API responses."""

from __future__ import annotations

from .zerox_terminal_display import terminal_display


def interactive_view(text: str) -> None:
    """Display ``text`` in a pager with consistent Markdown rendering."""

    terminal_display(text, scroll=True, chatbot=True)
