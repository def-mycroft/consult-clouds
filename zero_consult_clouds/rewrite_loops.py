import re
from datetime import datetime
from pathlib import Path
from typing import Callable, List

from .chat import ChatGPT
from .config import CONFIG_FILE


_DEFAULT_MAX_ITER = 5


def _parse_sections(text: str) -> tuple[str, str]:
    parts = re.split(r"\n\*\*\*\n", text, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    # fallback: split roughly in half
    lines = text.splitlines()
    mid = len(lines) // 2
    return "\n".join(lines[:mid]).strip(), "\n".join(lines[mid:]).strip()


def _dummy_send(prompt: str) -> str:
    return "dummy response"


def _safe_send(prompt: str) -> str:
    return "safe mode: no api call"


def iterative_rewrite(
    input_file: Path,
    *,
    config_path: Path = CONFIG_FILE,
    max_iter: int = _DEFAULT_MAX_ITER,
    safe: bool = False,
    dummy: bool = False,
) -> List[Path]:
    text = input_file.read_text(encoding="utf-8")
    draft, context = _parse_sections(text)

    if dummy:
        send: Callable[[str], str] = _dummy_send
    elif safe:
        send = _safe_send
    else:
        chat = ChatGPT(config_path=config_path)
        send = chat.send
    interactive = not (safe or dummy)

    summary = send(
        "Summarize the purpose and fitness goals in 5 bullet points:\n" + context
    )
    print(summary)
    if interactive:
        cont = input("Continue? [y/N] ").strip().lower()
        if cont != "y":
            return []

    versions: List[str] = [draft]
    output_paths: List[Path] = []
    out_dir = input_file.parent
    for i in range(1, max_iter + 1):
        if interactive:
            comments = input("Comments (or 'q' to quit): ").strip()
            if comments.lower() == "q":
                break
        else:
            comments = ""
        prompt = (
            "Rewrite the following draft to better meet the purpose. "
            "After the rewrite, provide 5 bullet points describing the changes.\n"
            f"Context:\n{context}\nComments:\n{comments}\nDraft:\n{versions[-1]}"
        )
        result = send(prompt)
        lines = result.strip().splitlines()
        bullet_idx = next((j for j, l in enumerate(lines) if l.startswith("-")), len(lines))
        new_text = "\n".join(lines[:bullet_idx]).strip()
        bullets = "\n".join(lines[bullet_idx:]).strip()
        fname = f"convo-{datetime.utcnow():%Y%m%d}-v{i}.md"
        out_path = out_dir / fname
        out_path.write_text(new_text, encoding="utf-8")
        output_paths.append(out_path)
        print(bullets)
        versions.append(new_text)
        if interactive:
            again = input("Another iteration? [y/N] ").strip().lower()
            if again != "y":
                break
        else:
            break

    final_prompt = (
        "Score each version on fitness criteria and explain briefly.\n" +
        context + "\n" + "\n".join(
            f"Version {idx}:\n{v}" for idx, v in enumerate(versions)
        )
    )
    final = send(final_prompt)
    print(final)
    return output_paths


__all__ = ["iterative_rewrite"]
