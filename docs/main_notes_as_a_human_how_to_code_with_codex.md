# As a Human: How to Code with Codex

#process-notes
random codename: afraid-award b7af63fb

***

This article distills the workflow used throughout the `zero-ai-dev-framework` project to develop code with Codex. It is based on the various prompt documents and notes in this repo.

## Overview

The key idea is to treat Codex as a collaborator that works best with tightly scoped prompts and rich written context. Development proceeds in layers: small features are added through short prompts, while larger tasks are captured in standalone `docs/prompt*_*.md` files referenced by codename.

## Workflow Steps

1. **Start with Documentation**  
   - Describe the desired change or feature in a Markdown file inside `docs/`.  
   - For substantial updates, create a new `prompt` file (e.g. `prompt7_new_feature.md`) and generate a codename using `helpers.codename()`.  
   - Refer to this codename when instructing Codex, e.g. "follow instructions in doc with codename *hilarious-consist 534ec3a9*."
2. **Craft Focused Prompts**  
   - Break functionality into testable units: a single function, class, or bug fix.  
   - Include only the necessary context or file snippets.  
   - Link to existing docs for background rather than repeating large blocks of text.
3. **Iterate Recursively**  
   - Ask Codex to implement or modify code according to the prompt.  
   - Inspect the diff and refine instructions if the result is incomplete.  
   - Continue the loop until the feature meets the spec.
4. **Write and Run Tests**  
   - Whenever new behavior is introduced, create or update unit tests in `tests/`.  
   - Run `pytest` after changes to ensure the suite passes before committing.
5. **Document Insights**  
   - Summarize design decisions or tricky behavior in the wiki.  
   - Keep the docs short but explicit so future prompts can reference them.
6. **Update the Table of Contents**  
   - Execute `zero-ai-dev-framework dev --update-toc` to regenerate `docs/CONTENTS.md` whenever docs are added or renamed.
7. **Commit Cleanly**  
   - Review diffs, remove stray edits, and ensure docstrings follow the style guide.  
   - Commit related code and docs together with a concise message.

## Why This Works

Writing prompts in the repo keeps a persistent record of what Codex was asked to do. The codename reference allows complex instructions to be reused without pasting them repeatedly. By layering small changes and documenting context, the developer can evolve the simulator while maintaining clarity and test coverage.
# Git Info
Commit: 43db73f7df84193785b045c7924387d0090ba6e5
Date: 2025-06-12T10:20:31-07:00

