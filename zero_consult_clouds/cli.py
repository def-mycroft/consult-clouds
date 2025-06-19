import argparse
from pathlib import Path
from typing import Callable, List
from uuid import uuid4 as uuid
from codenamize import codenamize


from .chat import ChatGPT, write_history
from .helpers import extract_template_vars, load_asset_template, codename
from .interactive_fill import interactive_fill
from .config import CONFIG_FILE, load_config, setup_config
from .rewrite_loops import iterative_rewrite
from .docs_tools import update_toc, new_doc


def _cmd_util(options: argparse.Namespace) -> int:
    """Handle the ``util`` sub-command."""

    if options.fill_template:
        print('this is hard coded to filling out writing_product for now')
        t = load_asset_template(str(options.fill_template))
        d = extract_template_vars(t)
        fp = interactive_fill({'fp_writing_product':0})['fp_writing_product']
        with open(fp, 'r') as f:
            writing_product = f.read()
        d['uuid'] = str(uuid())
        d['codename'] = codenamize(d['uuid'])
        d['writing_product'] = writing_product
        fp = options.output_filepath
        with open(fp, 'w') as f:
            f.write(t.render(d))
        print(f"wrote '{fp}")



def _cmd_setup_config(options: argparse.Namespace) -> int:
    """Handle the ``setup-config`` sub-command."""

    interactive = not options.non_interactive
    try:
        setup_config(
            path=options.config,
            api_key=options.api_key,
            default_model=options.model,
            interactive=interactive,
        )
    except Exception as exc:  # pragma: no cover - unexpected
        print(f"error: {exc}")
        return 1
    return 0


def _cmd_convo(options: argparse.Namespace) -> int:
    """Handle the ``convo`` sub-command."""

    try:
        text = options.file.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"error reading {options.file}: {exc}")
        return 1

    try:
        cfg = load_config(options.config)
        chat = ChatGPT(config_path=options.config)

        if options.promptlib_pretext:
            if cfg.promptlib_dir is None:
                raise RuntimeError("promptlib_dir not configured")
            for pre in options.promptlib_pretext:
                matches = list(Path(cfg.promptlib_dir).glob(f"*{pre}*"))
                if len(matches) != 1:
                    raise RuntimeError(
                        f"expected one match for {pre}, found {len(matches)}"
                    )
                pre_text = matches[0].read_text(encoding="utf-8")
                text = pre_text + "\n***\n" + text

        reply = chat.send(text)

        if options.output is not None:
            out_path = options.output
        else:
            if cfg.default_output_dir is None:
                raise RuntimeError(
                    "output file required and default_output_dir not set"
                )
            out_path = Path(cfg.default_output_dir) / "output.md"

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(reply, encoding="utf-8")

        if not options.disable_history_write:
            write_history(text, chat.last_response, output_dir=out_path.parent)
    except Exception as exc:  # pragma: no cover - unexpected
        print(f"error: {exc}")
        return 1
    return 0


def _cmd_dev(options: argparse.Namespace) -> int:
    """Handle the ``dev`` sub-command."""

    if options.new_doc:
        try:
            new_doc(docs_dir=options.docs_dir)
        except Exception as exc:  # pragma: no cover - unexpected
            print(f"error: {exc}")
            return 1

    if options.update_toc:
        try:
            update_toc(docs_dir=options.docs_dir)
        except Exception as exc:  # pragma: no cover - unexpected
            print(f"error: {exc}")
            return 1

    return 0


def _cmd_loops(options: argparse.Namespace) -> int:
    """Handle the ``loops`` sub-command."""

    print(options.file)
    input('here? >')
    if str(options.file) == 'i':
        k = 'fp_ path to input prompt (use zcc util -t) > '
        x = interactive_fill({k:0})
        options.file = x[k]
    try:
        iterative_rewrite(
            Path(options.file),
            config_path=options.config,
            safe=options.safe,
            dummy=options.dummy,
        )
    except Exception as exc:  # pragma: no cover - unexpected
        print(f"error: {exc}")
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Create and return the top-level :class:`argparse.ArgumentParser`."""

    parser = argparse.ArgumentParser(prog="zero-gptcli-clouds")
    subparsers = parser.add_subparsers(dest="command", required=True)

    util_parser = subparsers.add_parser("util")
    util_parser.add_argument("--output-filepath", "-f", type=Path,
                             default="/l/tmp/prompt.md")
    util_parser.add_argument("--fill-template", "-t", type=Path,
                             default="")
    util_parser.set_defaults(func=_cmd_util)

    cfg_parser = subparsers.add_parser("setup-config")
    cfg_parser.add_argument("--config", type=Path, default=CONFIG_FILE)
    cfg_parser.add_argument("--api-key")
    cfg_parser.add_argument("--model", default="gpt-3.5-turbo")
    cfg_parser.add_argument("--non-interactive", action="store_true")
    cfg_parser.set_defaults(func=_cmd_setup_config)

    convo_parser = subparsers.add_parser("convo")
    convo_parser.add_argument("-f", "--file", type=Path, required=True)
    convo_parser.add_argument("-o", "--output", type=Path)
    convo_parser.add_argument("--config", type=Path, default=CONFIG_FILE)
    convo_parser.add_argument("--disable-history-write", action="store_true")
    convo_parser.add_argument("--promptlib-pretext", action="append")
    convo_parser.set_defaults(func=_cmd_convo)

    loops_parser = subparsers.add_parser("loops")
    loops_parser.add_argument("-f", "--file", type=Path, required=True)
    loops_parser.add_argument("--config", type=Path, default=CONFIG_FILE)
    loops_parser.add_argument("--safe", action="store_true")
    loops_parser.add_argument("--dummy", action="store_true")
    loops_parser.set_defaults(func=_cmd_loops)

    dev_parser = subparsers.add_parser("dev")
    dev_parser.add_argument("--update-toc", action="store_true")
    dev_parser.add_argument("--new-doc", action="store_true")
    dev_parser.add_argument("--docs-dir", type=Path)
    dev_parser.set_defaults(func=_cmd_dev)

    return parser


def main(argv: List[str] | None = None) -> int:
    """Entry point used by ``python -m zero_consult_clouds``."""

    arg_parser = build_parser()
    parsed_args = arg_parser.parse_args(argv)
    handler: Callable[[argparse.Namespace], int] | None = getattr(
        parsed_args, "func", None
    )
    if handler is None:
        arg_parser.print_help()
        return 1
    return handler(parsed_args)


__all__ = ['main', 'build_parser']
