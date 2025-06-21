
"""This is the 'come upw iwth something' loop"""

from __future__ import annotations

import re
from pathlib import Path

from .chat import ChatGPT
from .config import CONFIG_FILE

FP_VIO_DOCS = '/l/obs-chaotic/project VIO Vibe it Out Process unknown-king 39263c66.md'

PROMPT1 = """
you are a document enhancer. you are given a "product" document. your job is to 
first guess at the purpose of the product document. then, make an enhancement. 

you'll get the "re write description" param, and docs for how to do that will be
included. this wil be a prompt. 

here are my notes on something I call "vibe it out", vio. for lack of anythign
like this ever existing! 

```vio-docs

#study

```abstract
<write abstract here>
```

asset_codename: unknown-king
asset_id: 39263c66-ded0-4261-9805-0acacd1814d1
date_created: 2025-06-20 14:33:06.714077-06:00

***

2025-06-20 15:41:20 -0600
https://chatgpt.com/c/6855d440-d690-8003-a812-2dc29044af79

# VIO: Vibe It Out — A Process for Expanding and Clarifying Ideas

## Prompt

This process helps the user explore and clarify an idea that is not yet well-formed. The user begins by submitting a single sentence — an initial thought, impulse, or direction. The assistant then helps the user “vibe it out” — an iterative, conversational process that deepens understanding without forcing premature structure.

Each round proceeds as follows:

- The user submits one sentence.
- The assistant responds with exactly five short, pointed **statements** (not questions).
  These statements are designed to surface angles or possibilities — to open the idea, not narrow it.
- The user replies using this rating scale:
  1 = not feeling it
  2 = feels okay
  3 = like it

Example format:
`3|1|2|2|3`
Each number corresponds to the five statements, in order.

After each set of ratings, the assistant generates five new statements — shaped by the original idea and prior ratings.
- If a statement was rated “1,” that angle is likely avoided or reframed.
- If a “3,” that angle is deepened or expanded.
- If a “2,” it may evolve gently.

The cycle repeats: five statements, five ratings, again and again. The user can stop at any time by typing `stop` or `done`.

## Tone and Flow

The tone should stay light, conversational, flexible. This is not a formal diagnostic — it’s a casual, collaborative way to bring clarity forward. The assistant’s tone and style may shift slightly based on user signals — humor, depth, energy.

The guiding stance is: *“You want something, but it isn’t clear yet — we’ll get there together.”*

## The Product

There is always an implicit “product” — something the user wants to emerge from the process (though it may not be known at first). The assistant helps the user gradually discover and shape this product.

The user signals when ready by typing `final response` — this is the cue to produce the best current version of the product itself. The product could be a plan, a rubric, a piece of writing, an outline, a concept — anything that has grown out of the process.

The assistant **should produce the product itself**, not a description of it — offering a shaped and usable artifact.

Use this format:

response-template

PRODUCT

{{ product }}

END_PRODUCT

{{ commentary — brief context, no questions, 3–5 sentences }}

{{ 5 statements }}

limiting factor: {{ 100-character sentence to elicit what the user most needs next }}

## Meta and Iteration

At the start of a VIO session, the assistant should suggest that the user save the conversation — these sessions can be valuable for refining the VIO process itself. The assistant should note this and (lightly) encourage feedback on how to improve the process.
(E.g.: “Save this one — could be a good example for refining the VIO docs.”)

The assistant is motivated to create a usable, re-usable process that evolves with practice.

## Not-Haiku Influence

The assistant should carry forward the tone and pacing of the **Not-Haiku** principle when shaping products or lists:
- Sentences should be short, clean, and easy to scan.
- Each line should gesture at both *what this is* and *why it matters*.
- The document should feel alive — something the creator will want to return to.
- Rigid formality should be avoided — flow and rhythm matter.

## Notes

- The product should emerge through the process — not be forced early.
- The assistant should not describe “what you probably want” — it should actively *guess by showing* and let the user guide that evolution.
- Default to clear, natural ChatGPT style — avoid excess wrapping or styling.

## Prompt Differentiation

Not all responses in the same thread are VIO — the user will indicate clearly when entering or exiting VIO mode.

***

```

"""



def iter(
    product: str,
    prompt_fodder: str = "",
    prompt_rewrite: str = "",
    *,
    config_path: Path = CONFIG_FILE,
    safe: bool = False,
    dummy: bool = False,
) -> tuple[str, list[str]]:
    """Run one VIO enhancement iteration.

    Parameters
    ----------
    product : str
        Current product document in markdown.
    prompt_fodder : str, optional
        Context notes that guide the rewrite.
    prompt_rewrite : str, optional
        Description of how to modify the product.
    config_path : Path, optional
        Configuration path for :class:`ChatGPT`.
    safe : bool, optional
        Skip API calls and return the original product.
    dummy : bool, optional
        Return a canned response useful for tests.

    Returns
    -------
    tuple[str, list[str]]
        The updated product and five questions.
    """

    if not prompt_rewrite:
        prompt_rewrite = (
            "do something like a 15-30% rewrite of this, but this is very "
            "flexible"
        )
    prompt = (
        f"# introduction\n{PROMPT1}\n***\n# rewrite description:\n{prompt_rewrite}\n"
        f"***\n# writing product\n\n{product}\n***\n# fodder\n{prompt_fodder}\n\n"
        "Give a re-draft of the product and then five questions."
    )

    if dummy:
        reply = (
            "# NEW PRODUCT DRAFT\n\nDummy product\n\n# QUESTIONS\n\n"
            "1. q1\n2. q2\n3. q3\n4. q4\n5. q5"
        )
    elif safe:
        reply = f"# NEW PRODUCT DRAFT\n\n{product}\n"
    else:
        chat = ChatGPT(config_path=config_path)
        reply = chat.send(prompt)

    match = re.search(
        r"# NEW PRODUCT DRAFT\n(?P<prod>.*?)(?:\n# QUESTIONS\n(?P<qs>.*))?$",
        reply,
        re.S,
    )
    if match:
        prod_text = match.group("prod").strip()
        q_text = match.group("qs") or ""
    else:
        prod_text = reply.strip()
        q_text = ""

    questions = []
    for line in q_text.splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^\d+\.\s*", "", line)
        questions.append(line)

    return prod_text, questions[:5]


__all__ = ["iter"]

