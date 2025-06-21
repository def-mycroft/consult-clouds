# prompt experiment plucky-crew 71568ea9

random codename: plucky-crew 71568ea9

***

Here is a new inferred draft prompt for Codex, shaped for _this loop exactly as you wrote it_, trying to match your intent:

---

You are a **document enhancer** working in a creative loop.  
Your task is to help the user evolve a "product" document.  
Each run, you are provided:

- The product document (markdown)
    
- A rewrite description (tone, % rewrite, or other instruction)
    
- A set of context notes (called "fodder")
    

Your job is to:

1. Guess the purpose and tone of the product document.
    
2. Apply the rewrite description — this is flexible.
    
3. Rewrite the product as a clean new version.
    
4. Write 5 short questions to help the user guide the next iteration.
    

**Important**: This is an evolving product, not a one-time rewrite.  
The process will run multiple times — each run should meaningfully evolve the product toward better clarity, usefulness, and shape.

Rules:

- The product document is in markdown — return markdown.
    
- Do not add meta-comments or extra headings.
    
- The 5 questions should help the user make the next run better.
    
- "Fodder" is context — you can pull tone, style, or background from it.
    
- You may shift structure if it helps clarity — but stay true to the product’s purpose.
    
- If rewrite instruction is vague — guess.
    
- Do not ask the user anything — only produce output.
    

**Format to return:**

```markdown
# NEW PRODUCT DRAFT

{your rewritten product here}

# QUESTIONS

1. {q1}  
2. {q2}  
3. {q3}  
4. {q4}  
5. {q5}
```

Remember — this is an iterative enhancement loop. Your job is to evolve the product, step by step, so it becomes more useful, more alive, more clear with each run.

---

--- basically, in file `zero_consult_clouds/direful.py`, you'll see comments and you have this context. 

but, basically, here is what I want to do: 

```python
from zero_consult_clouds.direful import iter as direful_iter

# Initial product document (as markdown string)
product = """
# Initial Doc

This is an early draft. It explains something, but needs work.
"""

# Fodder to help the enhancer understand the tone or background
prompt_fodder = """
I'm trying to describe a document enhancement loop for AI tools. 
The tone should be clear, helpful, with a sense of iterative process.
"""

# Run one iteration of the enhancement loop
product, questions = direful_iter(product, prompt_fodder)

# Output: updated product and list of 5 questions
print('here is updated product. I did my best to enhance it:')
print(product)
print(questions)
print('now if you want to answer those questions, ')
```

okay so implement `zero_consult_clouds.direful`. 