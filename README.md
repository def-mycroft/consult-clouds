# Utilities for Interacting with openai APIs 

run `pip install -e . ` and then you should have `zero-consult-clouds --help`. 

To ask chatgpt a question and get a response, use `zero-consult-clouds convo -f /l/tmp/input.md -o /l/tmp/output.md`.

The CLI now includes a basic `promptlib` manager for browsing and viewing prompt
files:

- `zero-consult-clouds promptlib browse` opens an interactive picker.
- `zero-consult-clouds promptlib cat <uuid>` prints a prompt by UUID.
- `zero-consult-clouds promptlib stats` shows library statistics.

