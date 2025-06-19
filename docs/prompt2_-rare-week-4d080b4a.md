# prompt2 xxx rare-week 4d080b4a

random codename: rare-week 4d080b4a

***



---
# initiation

You are updating a CLI project. 

## update config 

The default config.yaml contains keys such as `default_model`. You will update it so the key is named `model` (rename `default_model` → `model`) and add a new key `model-tokenmax`. Set its value based on the current model. For `gpt-4o`, set `model-tokenmax: 128000`.

## implement helper 

You will also implement a new helper function:

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))
```

Integrate this into the project's helpers module.

## update deps

Update the project’s dependencies to include `tiktoken` and ensure it installs with the project (setup.py, requirements.txt, pyproject.toml, or other—match project conventions). If dependencies are managed in multiple places (env.yaml, etc.), update all relevant ones.

## chunk content

content must be properely set up to send to openai endpoints, i.e. if more than token max, needs to be set up in a certain way. 

-- note : I"m not sure how to best integrate this functionality, just keep to larger principles listed here and in docs. it def needs to be somewhat isolated because this stuff is buggy. tests shoudl be extra clar. 

Now that the config includes `model-tokenmax` and you have a `count_tokens` helper, implement functionality in a new module `chunking_processor` to break large input content into multiple token-safe chunks. The chunking logic should ensure that each resulting chunk is smaller than `model-tokenmax`, leaving room for prompt tokens and system messages. You should design chunking to preserve as much natural structure as possible (for example, preferring to break on paragraph or sentence boundaries rather than mid-word or mid-sentence). This will allow large documents (such as books or reports) to be processed incrementally while respecting model constraints.

## context importance

When breaking content into N chunks, all N chunks must be available to the model as context. The goal is _not_ to multiply API calls or process chunks independently, but to enable the application to submit the relevant prior chunks along with the current chunk, so that the model retains proper context across the entire document. The `chunking_processor` module should provide functionality to assist with this, for example returning not just individual chunks but also the ability to construct message histories or context windows for each chunk submission.
## pass tests 


After making changes, run the existing project tests (unit and integration). All tests must pass.

## additionally 

You do not need to rewrite or refactor unrelated project parts. You will update only config, helpers, dependencies, and tests.

## docs 

add a docs/ article `tutorial-rare-week 4d080b4a.md`  with a tutorial which shows how chunking works with this code. make sure to note the commit on when that docs was added (latest before integrated). rare-week 4d080b4a

---

