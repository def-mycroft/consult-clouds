
# Project Purpose and Scope

Clearly define the tool’s primary goal, which is to create a reusable, installable module and command-line interface that wraps interaction with a language model API. Describe what the user will gain from using the tool (e.g., automation, scriptability, repeatable prompt runs). Clarify any assumptions, such as the use of OpenAI’s API or other compatible services. This section should focus on user needs and the tool’s intended role in a larger workflow.

# Core Functional Requirements

Specify the main pieces of functionality the tool must implement—such as maintaining conversation history, using config files, and exposing CLI commands for setup and prompt execution. Explain what each component does in abstract terms without binding to any specific code. The focus should be on describing what behaviors are required, not how they should be implemented. This sets the design targets for the module and CLI parity.

# Structural and Modular Design

Describe the layout of the codebase in terms of logical separation: configuration handling, API logic, and CLI tooling should be distinct. Emphasize the value of clear, orthogonal modules that encapsulate responsibility and simplify future edits. Explain that names, folder organization, and division of logic are not arbitrary but essential to maintainability and clarity. This section frames the architectural principles guiding the implementation.

# Interface Contracts

Define the expected behavior of major public-facing objects and functions (e.g., the `send()` method should track context and return a reply). Capture how state is managed internally and how user inputs flow through the system. Where relevant, note performance, error-handling, or user-experience constraints that need to be preserved across both CLI and programmatic usage. Keep this focused on observable behavior, not implementation mechanics.

# Extensibility and Future-Proofing

Describe how the initial structure should remain adaptable to future functionality, such as embedding, summarization, or model-switching. Encourage use of hooks, base classes, or loosely coupled modules so features can be expanded without rewrites. Mention the importance of version control, semantic naming, and configuration conventions that accommodate growth. This section guides forward-looking architectural decisions.

# Usability and Resilience

Articulate the user experience expectations—e.g., setup must be intuitive, errors should be actionable, and CLI should fail gracefully with helpful output. The focus here is on clarity, predictability, and robustness in how users interact with the system. Include advice to test for common misconfigurations and catch exceptions early. This section serves as a reminder to prioritize the developer experience alongside functionality.

# Testing and Quality Signals

Outline how to construct basic test cases without overprescription: validate end-to-end prompts, simulate config generation, ensure CLI-file I/O flows work as expected. Emphasize that tests are also a signal of design quality, not just correctness. Note that coverage of edge cases, meaningful error assertions, and sanity checks on outputs are more valuable than exhaustive low-level unit tests. Keep this section open-ended to allow intelligent interpretation during development.


***
#############################################################################################################

# Project Launch Prompt

***

You are setting up a Python project scaffold named `zero-consult-clouds` that provides both a reusable module and CLI for interacting with OpenAI's API.

## GOAL

Build a pip-installable Python module `zero_consult_clouds` that:

1. Provides a `ChatGPT` class to manage an OpenAI conversation. It should maintain conversation context across multiple `.send()` calls, appending messages to the history and returning the assistant’s reply.
2. Uses a config file (`~/.config/zero_consult_clouds/config.json`) to store API keys and model preferences. Add a CLI command `zero-gptcli-clouds --setup-config` to generate this file if missing.
3. Exposes a CLI tool `zero-gptcli-clouds` with a subcommand `convo` to send a prompt from a file (`-f INPUT.md`) and save the reply to another file (`-o OUTPUT.md`).
4. Designed for extensibility, the base structure should allow future addition of functionality like summarization, embedding, cost estimation, or vector store RAG.

# PROJECT STRUCTURE

Create a layout like this:

```
zero-consult-clouds/
├── pyproject.toml
├── setup.cfg
├── zero_consult_clouds/
│   ├── __init__.py
│   ├── chat.py       # defines ChatGPT class
│   ├── config.py     # handles loading and writing config
│   └── cli.py        # CLI logic
└── entry_points      # defined in pyproject.toml or setup.cfg
```

# MODULE FUNCTIONALITY

**ChatGPT class**

* Constructor should accept an optional config or load from default path.
* `.send(prompt: str) -> str` appends prompt to internal context, sends API call, appends reply, and returns reply.
* `.get_context() -> list` returns the current message history.
* Support optional max\_tokens and model override.

**Config**

* Use `~/.config/zero_consult_clouds/config.json` to store:

  * `api_key`
  * `default_model` (e.g., `gpt-4o`)
* `--setup-config` should create a skeleton config interactively or with defaults.

**CLI**

Expose via entry points in setup:

* `zero-gptcli-clouds --setup-config`
  Writes config file.

* `zero-gptcli-clouds convo -f input.md -o output.md`
  Loads input from markdown, sends prompt using ChatGPT, saves reply to output.

Use `argparse` or `click` in `cli.py` and `import ChatGPT` from the main module.

# DESIGN PRINCIPLES

Long-term extensibility. Building a foundation that cleanly accommodates future capabilities—whether summarization, embedding, cost estimation, or RAG—minimizes the need for disruptive rewrites as requirements evolve. By anticipating growth, you trade a small upfront architecture cost for vastly reduced future friction.

Separation of concerns. Isolating configuration management, API interaction, and CLI logic into distinct modules prevents inadvertent coupling. This clarity allows contributors to work on one area without risking regressions in others, and it simplifies unit testing by narrowing each component’s responsibilities.

Encapsulated conversation state. Treating the chat history as an internal, self-managed object within a `ChatGPT` class guards against context leaks and mismatches. This object-oriented approach ensures that every `.send()` call reliably reflects prior messages, a necessity when conversations span multiple turns or persist across different entry points.

CLI-programmatic parity. Ensuring that every feature available via the module API is exposed through the CLI (and vice versa) avoids divergent implementations. Consistent contracts between the class methods and CLI commands mean enhancements automatically flow to both interfaces, reducing duplication and maintenance overhead.

Resilient error handling and feedback. Turning opaque API failures or misconfigurations into clear, actionable messages transforms developer friction into informed next steps. By catching missing keys, invalid paths, or HTTP errors early, the tool becomes not just functional but trustworthy, fostering confidence for users and maintainers alike.


# TEST CASES

I don't want to specify too closely because I want you to influence 

```python
from zero
```

# NOTES

* Do not include unused code from earlier versions.
* Structure should be clean, Pythonic, and adhere to common project patterns.
* Add appropriate error handling (e.g., missing API key, invalid file paths).
* Add docstrings to major classes and functions.

