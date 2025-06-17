import argparse
from pathlib import Path
from typing import List

from .chat import ChatGPT
from .config import CONFIG_FILE, setup_config
from .docs_tools import new_doc, update_toc


def _cmd_setup_config(args: argparse.Namespace) -> int:
    interactive = not args.non_interactive
    try:
        setup_config(
            path=args.config,
            api_key=args.api_key,
            default_model=args.model,
            interactive=interactive,
        )
    except Exception as exc:  # pragma: no cover - unexpected
        print(f"error: {exc}")
        return 1
    return 0


def _cmd_convo(args: argparse.Namespace) -> int:
    try:
        text = args.file.read_text(encoding='utf-8')
    except Exception as exc:
        print(f"error reading {args.file}: {exc}")
        return 1
    try:
        chat = ChatGPT(config_path=args.config)
        reply = chat.send(text)
        args.output.write_text(reply, encoding='utf-8')
    except Exception as exc:  # pragma: no cover - unexpected
        print(f"error: {exc}")
        return 1
    return 0


def _cmd_dev(args: argparse.Namespace) -> int:
    if args.new_doc:
        try:
            new_doc(docs_dir=args.docs_dir)
        except Exception as exc:  # pragma: no cover - unexpected
            print(f"error: {exc}")
            return 1
    if args.update_toc:
        try:
            update_toc(docs_dir=args.docs_dir)
        except Exception as exc:  # pragma: no cover - unexpected
            print(f"error: {exc}")
            return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='zero-gptcli-clouds')
    sub = parser.add_subparsers(dest='command', required=True)

    cfg = sub.add_parser('setup-config')
    cfg.add_argument('--config', type=Path, default=CONFIG_FILE)
    cfg.add_argument('--api-key')
    cfg.add_argument('--model', default='gpt-3.5-turbo')
    cfg.add_argument('--non-interactive', action='store_true')
    cfg.set_defaults(func=_cmd_setup_config)

    convo = sub.add_parser('convo')
    convo.add_argument('-f', '--file', type=Path, required=True)
    convo.add_argument('-o', '--output', type=Path, required=True)
    convo.add_argument('--config', type=Path, default=CONFIG_FILE)
    convo.set_defaults(func=_cmd_convo)

    dev = sub.add_parser('dev')
    dev.add_argument('--update-toc', action='store_true')
    dev.add_argument('--new-doc', action='store_true')
    dev.add_argument('--docs-dir', type=Path)
    dev.set_defaults(func=_cmd_dev)

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    func = getattr(args, 'func', None)
    if func is None:
        parser.print_help()
        return 1
    return func(args)


__all__ = ['main', 'build_parser']
