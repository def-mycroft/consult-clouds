# Project Purpose and Scope

**prompt template utility:** *This section defines the problem space and value proposition of the tool with a focus on automatable workflows, providing Codex with the context to guide architectural decisions around usability, system boundaries, and user assumptions. It clarifies the end user's environment, expected behavior, and intended use cases, enabling Codex to generate solutions that are compatible with scripting, CLI automation, and modular Python development. This orientation grounds the code in a real deployment context, avoiding toy-level assumptions.*

The zero-consult-clouds project aims to deliver a pip-installable Python package and accompanying command-line interface that streamline multi-turn conversations with OpenAI’s API in scripted workflows. Users will gain a reusable ChatGPT client library for embedding chat logic in Python code and a CLI tool named zero-gptcli-clouds for easy configuration setup and file-based prompt execution. By assuming an existing OpenAI API key and Python 3.8+ environment on Ubuntu, the tool focuses on automating repeatable prompt runs, ensuring scriptability, and integrating seamlessly into larger data-processing or DevOps pipelines.

# Core Functional Requirements

**prompt template utility:** *This section tells Codex which features are essential and what behavioral guarantees each must satisfy. By articulating the expected lifecycle and logic of each component—conversation state, config persistence, CLI I/O—this acts as a behavioral contract. Codex can use this section to constrain its generation scope, ensuring only required features are implemented, and that optional ones remain modular and clearly separated.*

The package must implement three core behaviors: conversation management, configuration handling, and CLI command execution. Conversation management requires a ChatGPT class that maintains an internal history of messages, offers a send(prompt: str) method to append user input to context, invoke the API, append the model’s reply, and return that reply. Configuration handling must read and write a JSON file under ~/.config/zero_consult_clouds/config.json storing at least an api_key and default_model, and offer an interactive or scripted setup flow. CLI command execution should expose a setup-config command that creates or updates the config file when missing, and a convo command that reads a markdown file as input, sends its contents through the ChatGPT class, and writes the response to a specified output file.

# Structural and Modular Design

**prompt template utility:** *Codex should use this section to determine how to structure the physical layout of files and the architectural division of responsibilities. By following the specified module boundaries—chat, config, CLI—it can organize functionality in a way that preserves isolation of concerns and allows each layer to evolve independently. Codex should avoid collapsing responsibilities into monoliths or distributing logic inconsistently across files.*

The repository will separate responsibilities into distinct modules to maximize clarity and maintainability. Project metadata files like pyproject.toml and setup.cfg live at the root alongside README and LICENSE. Inside the zero_consult_clouds package, chat.py encapsulates the ChatGPT class and API logic, config.py manages loading, validation, and writing of configuration data, and cli.py handles command-line argument parsing and dispatch to library functions. Entry points declared in project metadata map zero-gptcli-clouds commands to functions in cli.py, ensuring a single implementation surface for both library and CLI.

# Interface Contracts

**prompt template utility:** *Codex should interpret this section as defining expected input/output semantics and failure modes for public interfaces. It provides rules for argument validation, error propagation, and runtime guarantees, ensuring that Codex-generated code conforms to user expectations for type safety, composability, and fault clarity. This guidance enables the assistant to build robust methods with clearly defined responsibilities and predictable external behavior.*

Public interfaces must behave predictably and document state transitions clearly. The ChatGPT class constructor accepts an optional path to a config file or defaults to ~/.config/zero_consult_clouds/config.json, raising a clear error if required fields are missing. The send method consumes a text prompt and optional model or token overrides, updates internal history, and returns a string reply or raises a descriptive exception on API failure. Config functions load and return a simple namespace or dict, and write updates atomically to disk. CLI functions return exit codes: zero on success, nonzero on user or system errors, and print human-readable messages when encountering invalid paths, missing keys, or HTTP errors.

# Extensibility and Future-Proofing

**prompt template utility:** *Codex should use this section to shape abstractions and boundaries with growth in mind. Instead of hardcoding logic, it should expose clearly marked interfaces, opt-in customization points, and avoid premature coupling between modules. This section gives Codex permission to scaffold for generality, even when a use case isn’t yet implemented, as long as it doesn’t compromise simplicity for the current feature set.*

The initial design anticipates future features by keeping modules loosely coupled and exposing extension points. The ChatGPT class may inherit from a base client class or accept middleware hooks, allowing embedding, summarization, or vector-store retrieval layers to be grafted without modifying core logic. Configuration conventions support semantic versioning and ignore unrecognized keys, so new options can be introduced without breaking existing installations. A clear module hierarchy and naming scheme will guide contributors on where to place new capabilities, preserving code readability and reducing the risk of regressions.

# Usability and Resilience

**prompt template utility:** *Codex should rely on this section to shape user-facing behavior, including defaults, error messaging, and failure handling patterns. Rather than assuming silent errors or complex stack traces, Codex is expected to produce scripts that are self-healing where possible and always communicate clearly. This section authorizes Codex to prefer user guidance over raw tracebacks, and to design the control flow with practical UX in mind.*

Users should find configuration setup intuitive and error messages actionable. The setup-config command will detect missing or malformed configuration files and prompt the user for required values or fallback defaults. The convo command validates that input and output file paths exist or can be created, displaying concise suggestions for correction rather than raw tracebacks. All API and filesystem interactions are wrapped in try-except blocks at the top level of the CLI to ensure graceful exits, with logging or verbose flags available for deeper diagnostics when needed.

# Testing and Quality Signals

**prompt template utility:** *This section orients Codex toward writing verifiable code that anticipates and handles edge cases, rather than assuming clean paths or overfitting to the happy path. Codex should use this to plan for testability, simulate common failures, and provide test doubles or mocks when real service access is impractical. It also guides Codex to prioritize high-signal test coverage—behavioral and integration-level checks—over exhaustive low-level unit tests.*

Test suites will focus on representative end-to-end scenarios and meaningful error conditions rather than exhaustive unit coverage. Tests should simulate config generation using temporary directories, mock OpenAI responses in the ChatGPT class to validate history management and exception handling, and invoke the CLI with sample input and output files to assert correct exit codes and file contents. Edge cases like missing API keys, invalid JSON in config, unreachable API endpoints, and unwritable output paths should each produce clear, predictable error messages. These tests serve both as correctness checks and as design-quality signals for future maintainers.

# Software Design Principles 

**prompt template utility:** *The Software Design Principles section serves as implementation guidance for Codex, clarifying not just _what_ the system should do, but _how_ the code should be structured to ensure long-term clarity, maintainability, and adaptability. It encodes architectural preferences that might otherwise be implicit or buried in examples, making them explicit for consistency across contributors or future iterations. These principles also help Codex make decisions about abstraction boundaries, error handling style, and control flow conventions without requiring repetitive instruction. By anchoring development in context-specific priorities, the section reduces ambiguity and aligns code generation with the broader project philosophy.*

## Prefer composable modules with single responsibility

Each file in the package should encapsulate one domain of logic—API interaction, config IO, or CLI dispatch. This makes the codebase easier to test, extend, and debug, especially when other modules evolve. Future contributors can replace or augment one piece without disrupting others, minimizing regressions and reducing the surface area of breaking changes.

## Treat the CLI as a thin wrapper over core logic

The CLI should invoke library methods and never contain its own business logic. This encourages reuse, makes testing easier, and simplifies documentation. When the core logic changes, the CLI behavior updates automatically, eliminating divergence and ensuring consistent behavior across interfaces.

## Use explicit class-based state for conversation history

A class-based design (versus functional or global-state approaches) for the ChatGPT interface enables clean state tracking, supports future injection of middleware, and scales better to multi-convo scenarios. Functional patterns work well for stateless utilities but are ill-suited for managing evolving context in a mutable message history.

## Design for fail-closed configuration handling

Config access should fail early and loudly if required fields are missing or unreadable. Rather than continuing with fallbacks or silent defaults, the tool should alert users and halt, ensuring predictable behavior. This principle simplifies debugging and avoids opaque errors further downstream when configs are misapplied.

## Separate user feedback from control flow logic

Messages printed to stdout or stderr should be handled by a messaging layer or helper, not interwoven with control logic. This separation enables easier testing, clean redirection in CI or scripts, and future i18n or UX customization. Code clarity improves when logic and user-facing language are decoupled.

# Notes

* Follow PEP-8 conventions and document all public classes and functions with numpydoc-style docstrings.  
* Declare CLI entry points in pyproject.toml or setup.cfg to ensure zero-gptcli-clouds commands install correctly.  
* Ensure atomic writes when updating config.json to prevent partial configurations.  
* Omit any legacy code fragments from earlier drafts and remove unused dependencies.  
* Keep interactive prompts minimal so the tool can operate in both CI pipelines and local shells without modification.  

*** 