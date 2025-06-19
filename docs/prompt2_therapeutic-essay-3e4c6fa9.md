# prompt2 simple re-write loops therapeutic-essay 3e4c6fa9

random codename: therapeutic-essay 3e4c6fa9

***


---

you are codex. you are editing a well-designed cli codebase, invoked with `zero-consult-clouds convo -f /l/tmp/prompt.md`, which sends text prompts to openai api and processes the returned results. the user now wants a new capability added. here is what to implement:

the cli will process writing documents by iteratively rewriting and critiquing them through 2-5+ api loops. the input document will be a markdown file with two sections: (1) the writing product (ex: blog post, website paragraph), and (2) contextual description of its purpose and fitness criteria.

first api call extracts purpose: return 5 bullet points summarizing the purpose and fitness goals as understood. display these in terminal. user can terminate or continue.

if continuing, ask user for any comments on the understanding (text input). send another api call: first rewrite the writing product (v1), guided by the purpose/goals/comments. save result as markdown file to `output/convo-YYYYMMDD-v1.md`. also display 5 bullet points describing what was changed and why.

repeat: each iteration runs one improvement rewrite and one fitness critique (bullet points why it is "more fit to purpose"). user can terminate after any iteration. total up to 5 iterations per run.

finally, after iterations, send each version (v0 original, v1, v2...) to api for a "final judgment": ask the api to score each version on fitness criteria and explain briefly. display result to user.

add two switches: `--safe` runs without api calls (prints example text), `--dummy` mode forces simplified behavior and quick runs for testing.

you, codex, should implement this capability into the codebase, using existing abstractions, convenience funcs, logging, and architecture. the result should look and behave consistently with existing cli flows. implement this now.


*** 