# interactive_fill.py

import sys
import time
import os
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
CURSOR_BLINK = "\033[5m_\033[0m"

class PathCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        dirname = os.path.dirname(text) if text else "/"
        prefix = os.path.basename(text)

        try:
            entries = os.listdir(dirname)
            entries = [e for e in entries if e.startswith(prefix)]
            entries = sorted(entries)
            for e in entries:
                full_path = os.path.join(dirname, e)
                display = e + "/" if os.path.isdir(full_path) else e
                yield Completion(
                    display,
                    start_position=-len(prefix),
                    display_meta="dir" if os.path.isdir(full_path) else "file",
                )
        except Exception:
            pass

def interactive_fill(d: dict, prompt_title="Fill in the following fields:"):
    def print_header():
        print(f"""{BOLD}{CYAN}
===============================================================================
This form will ask you to fill in fields. 
If a field starts with 'fp_' or 'fp_dir_', it is a filepath or directory path. 
TAB will autocomplete segments. Use ENTER to confirm.
Valid files or dirs will show a ✔︎  when accepted.
Press 'v' after typing a path to open it in vim, then return to prompt.
===============================================================================
{RESET}""")

    print_header()
    print(f"\n{BOLD}{CYAN}=== {prompt_title} ==={RESET}\n")

    result = {}
    session = PromptSession()
    style = Style.from_dict({
        "": "#ffff66",  # brighter yellow
    })

    for k in d.keys():
        print(f"\n{MAGENTA}{BOLD}{k}{RESET}:")

        if k.startswith("fp_") or k.startswith("fp_dir_"):
            path_completer = PathCompleter()
            allow_dir = k.startswith("fp_dir_")

            while True:
                try:
                    user_input = session.prompt(
                        "Path (TAB, v=vim, ENTER=accept): ",
                        completer=path_completer,
                        complete_in_thread=True,
                        style=style,
                    ).strip()

                    if user_input.lower() == "v":
                        print(f"{RED}Type a path first to open in vim.{RESET}")
                        continue

                    user_input = os.path.expanduser(user_input)
                    user_input = os.path.abspath(user_input)

                    if user_input and os.path.exists(user_input):
                        if user_input.lower().endswith("v"):
                            continue  # ignore if user typed 'v' after path

                        print(f"{CYAN}[Press ENTER to accept, or type 'v' to edit in vim]{RESET}")
                        action = session.prompt("> ").strip().lower()

                        if action == "v":
                            subprocess.run(["vim", user_input])
                            continue

                        if os.path.isfile(user_input):
                            print(f"{GREEN}✔︎  File accepted:{RESET} {user_input}")
                            result[k] = user_input
                            break
                        elif os.path.isdir(user_input) and allow_dir:
                            print(f"{GREEN}✔︎  Directory accepted:{RESET} {user_input}")
                            result[k] = user_input
                            break
                        elif os.path.isdir(user_input):
                            print(f"{YELLOW}Directory selected, please select a file inside.{RESET}")
                        else:
                            print(f"{RED}Unknown path type, try again.{RESET}")

                    else:
                        print(f"{RED}Invalid path, try again.{RESET}")

                except KeyboardInterrupt:
                    print(f"{YELLOW}\nCanceled, moving on.{RESET}")
                    break

        else:
            sys.stdout.write(f"{YELLOW}")
            sys.stdout.flush()
            time.sleep(0.1)
            user_input = input(CURSOR_BLINK + " ")
            result[k] = user_input.strip()

    print(f"\n{BOLD}{CYAN}--- Done! ---{RESET}\n")
    return result

