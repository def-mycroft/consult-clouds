# Styleguide for Wiki Articles

#process-notes
random codename: robust-application a24d9a19

*** 

note to codex: when adding any kind of article in docs, this style guide should be followed 

# Markdown Documentation Style Guide

This guide defines the rules for writing Markdown-based documentation that will be rendered cleanly in both Obsidian and GitHub. It applies to all wiki pages, READMEs, and general documentation content authored within this project.

## 1. Line Wrapping

Do **not** wrap lines manually. Each paragraph should be a single unbroken line. This ensures compatibility with both GitHub and Obsidian, preserving editing fidelity and minimizing diff noise in version control.

## 2. Headings

Use ATX-style (`#`) headings. Only use one `#` for the document title. Subsections should follow a consistent progression (i.e., `##`, then `###`, etc.). Do **not** skip heading levels.

```
# Title of Document
## Section
### Subsection
```

## 3. Paragraphs and Spacing

Always leave a blank line between paragraphs, headings, lists, and code blocks. Do not indent paragraphs.

## 4. Emphasis

Use `*italic*` and `**bold**` (not underscores). Avoid excessive emphasis.

## 5. Lists

Use hyphens (`-`) for unordered lists and numerals followed by a period (`1.`) for ordered lists. Indent nested items by two spaces. Do not use asterisks or plus signs for bullets.

```
- Item one
- Item two
  - Subitem
```

## 6. Code

Use backticks for inline code: `` `example()` ``. Use fenced blocks with triple backticks (\`\`\`) for code blocks, and always specify the language if known:

````markdown
```python
def hello():
    return "hello"
```
````

Avoid using indented code blocks (four spaces) unless required for compatibility.

## 7. Links and Images

Use reference-style links only when the same URL is reused many times. Otherwise, use inline:

```
[GitHub](https://github.com)
```

For images, prefer descriptive alt text and relative paths where possible:

```
![Diagram of flow](images/flowchart.png)
```

## 8. Tables

Keep tables simple and legible. Use hyphens for alignment only when needed. Do not use HTML tables.

```
| Column A | Column B |
|----------|----------|
| Foo      | Bar      |
```

## 9. Frontmatter

If using YAML frontmatter (e.g., in Obsidian), place it at the very top and keep it minimal.

```
---
tags: [guide, reference]
created: 2024-09-01
---
```

## 10. File Naming and Organization

Use `kebab-case.md` for file names. Each document should have a clear purpose and reside in the appropriate directory. Avoid overly broad or ambiguous file titles.

## 11. Tone and Clarity

Write in clear, direct prose. Favor active voice. Use short sentences and concrete examples. Avoid marketing fluff, ambiguity, and jargon unless it's technical and required.

## 12. Metadata Blocks (Optional)

When documenting code, use fenced code comments to include metadata (especially for tools that might parse them).

````markdown
```python
# %% Description: This script normalizes input vectors.
```
````

