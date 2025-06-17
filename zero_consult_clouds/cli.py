import argparse
from pathlib import Path
from typing import List


from .chat import ChatGPT, write_history
from .config import CONFIG_FILE, load_config, setup_config
from .docs_tools import update_toc



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
        cfg = load_config(args.config)
        chat = ChatGPT(config_path=args.config)

        if args.promptlib_pretext:
            if cfg.promptlib_dir is None:
                raise RuntimeError("promptlib_dir not configured")
            for pre in args.promptlib_pretext:
                matches = list(Path(cfg.promptlib_dir).glob(f"*{pre}*"))
                if len(matches) != 1:
                    raise RuntimeError(
                        f"expected one match for {pre}, found {len(matches)}"
                    )
                pre_text = matches[0].read_text(encoding="utf-8")
                text = pre_text + "\n***\n" + text

        reply = chat.send(text)

        if args.output is not None:
            out_path = args.output
        else:
            if cfg.default_output_dir is None:
                raise RuntimeError("output file required and default_output_dir not set")
            out_path = Path(cfg.default_output_dir) / "output.md"

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(reply, encoding='utf-8')

        if not args.disable_history_write:
            write_history(text, chat.last_response, output_dir=out_path.parent)
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
    convo.add_argument('-o', '--output', type=Path)
    convo.add_argument('--config', type=Path, default=CONFIG_FILE)
    convo.add_argument('--disable-history-write', action='store_true')
    convo.add_argument('--promptlib-pretext', action='append')
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
