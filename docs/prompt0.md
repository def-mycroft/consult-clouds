

want to write a python module which facilitates interacting with the openai api. I have an existing module which shows the way in which I have been accomplishing this; here:

```python
"""

# TODO - integrate summarization of context. this comment isn't located in the
# right place but needed to get it out of head. basically would want to be able
# to generate a summary of the input context, a full summary. could also just
# start more integration of the booksum project into here. 

"""
from . import helpers as hp
from gpt_general.config import load_config
from .embeddings import WikiEmbedding 

import openai
from transformers import GPT2Tokenizer
from jinja2 import Template

from os.path import exists, dirname, basename, join, expanduser
from glob import glob
import pandas as pd
import numpy as np
import json


CONFIG = load_config()
MODEL = CONFIG['fancy_model']
with open(CONFIG['api_key_path'], 'r') as f:
    openai.api_key = f.read().strip()


def archive_text_obs(text, fn):
    """Archive convo to obsidian vault"""
    assert exists('/l/obs-chaotic'), '/l/obs-chaotic'
    fp = join('/l/obs-chaotic', fn)
    t = f"#changeable-invite-automatic-output\n{text.split('# Given Context')[0]}" 
    with open(fp, 'w') as f:
        f.write(t)
    print(f"wrote '{fp}'")


def archive_question(question, response, context, prompt, folder):
    """Archive question, answers and context
    # TODO - it would be useful to have the context of the names of the "chatpers"
    # i.e. wnat to be able to retrieve what the document is that was sent as context
    it would be useful to more quickly be able to understand what the context
    means here, not sure how "accurate" the context is.  

    """
    if not exists(folder):
        raise Exception(f"folder {folder} not there. ")
    tag = basename(folder)
    fp = hp.asset_path('question-archive.jinja2')
    assert exists(fp)
    with open(fp, 'r') as f:
        t = Template(f.read())
    text = t.render(dict(question=question, response=response, context=context,
                         prompt=prompt, tag=tag))
    fmt = '%Y%m%dT%H%M%S MST'
    d = pd.Timestamp.utcnow()
    fn = f"{d.timestamp()} - {d.tz_convert('America/Denver').strftime(fmt)} - question and response.md"
    fp = join(folder, fn)
    with open(fp, 'w') as f:
        f.write(text)
    print(f"wrote '{fp}'")
    archive_text_obs(text, fn)


def init_convo(message='you are a helpful assistant'):
    conversation = [
        {"role": "system", "content": message}
    ]
    return conversation


def new_message(message, conversation, model='', max_tokens=2000,
                prompt_cost=False):
    """
    # TODO - kinda need to reformulate this to not be adhoc
    """
    if not model:
        model = MODEL

    # add preamble to message
    # TODO - this should be a config param and template (message prefix)
    message = f"relying as much as possible on the given context; {message}"
    conversation.append({"role": "user", "content": message})

    if prompt_cost:
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        n_tokens = len(tokenizer.tokenize(str(conversation)))
        print()
        print('the following is directly before making costly api call. ')
        hp.estimate_price(n_tokens, model=MODEL)
        input('continue? (any)... ')

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=conversation,
        max_tokens=max_tokens,
    )
    reply = response['choices'][0]['message']['content']
    conversation.append({"role": "assistant", "content": reply})
    d = {
        'convo':str(conversation),
        'message':message,
        'reply':reply,
    }
    
    return conversation, reply


def chat(query, w, folder_output='/l/tmp', full_context=False):
    if not full_context:
        # parse context, i.e. apply RAG
        context = w.retrieve_relevant_chunks(query, n=CONFIG['convo_chunk_context'])
    else:
        # give full context
        context = str(w.pages)
    convo = init_convo(message='your job is to read large amounts of text and '
                       'find key concepts in that text. more instructions will '
                       'follow. ')
    with open(hp.asset_path('convo-preface.jinja2'), 'r') as f:
        prompt = Template(f.read()).render({'context':context, 'prompt':query})
    convo, reply = new_message(prompt, convo, model=MODEL)
    archive_question(query, reply, context, prompt, folder=folder_output)

    return reply


def dialogue(path_text_input, output_folder, prompt='', disable_dialogue=False, 
             full_context=False):
    """Dialogue tool
    # TODO - would also be nice to understand how much the queries are costing
    """
    print(f"loading index...")
    w = WikiEmbedding(path_text_input=path_text_input)

    print(f"...done. ")
    if prompt:
        disable_dialogue = True
        response = chat(prompt, w, folder_output=output_folder,
                        full_context=full_context)
        r = response
        print()
        print(prompt)
        print(f"response: \n{'#'*80}\n{r}\n{'#'*80}\n")

    if not disable_dialogue:
        while True:
            q = input('input question > ')
            response = chat(q, w, folder_output=output_folder,
                            full_context=full_context)
            r = response
            print()
            print(q)
            print(f"response: \n{'#'*80}\n{r}\n{'#'*80}\n")
            input('continue? ')

```

the above was written in related to another project. don't copy any of this, this is here just for a weak reference to form your solution to the prompt I'm writing here.

module rquirements:

* make it possible to import something from this module (once installed btw this must be an installable module), use a function/method whatever it is to send text, receive text back, and continue the conversation with the full context of the convo. so I should be able to have some object like "context" and somehow append to it. but this is the most important thing: "use a function/method whatever it is to send text, receive text back, and continue the conversation with the full context of the convo."

- this should be scaffolding for a larger project that interacts w/ openai apis in general.

- installing this should also create the ability to do `zero-gptcli-clouds convo --prompt -f /l/tmp/input.md -o /l/tmp/response.md`, which loads the file, makes an api call and writes the single response to the output file specified by -o.

- provide a cli func `zero-gptcli-clouds --setup-config` which will write a default config to `~/.config`. the config should be written in

I'm thinking this should be class-based, e.g. there is a class ChatGPT which provides methods that interact w/ API.


--- write an optimal prompt for codex to use to set up this project. infer from where I'm at (i.e. the current (above) prompt) to a detailed prompt that is optimized for launching a  project such as this. 


