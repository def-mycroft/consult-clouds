# prompt4 implement start of promptlib  imperfect-drive 6a6433cf

random codename: imperfect-drive 6a6433cf
#prompt 
***


# outcome visualizations 

we'll start w/ the goal in mind: I'm going to desribe an update to this codebase and you're going to modify it. it is as if you're a painter and I'm describing what I want you to paint. neither of us know what we even can/want to do at this point, but I'm giving you ideas and sketches. 

this is what I'll be able to do after you finish this prompt. 

so, this section isn't necessarily "etched in stone", but at the same time this should have a lot of influence over how you draft this prompt 
## Usage Examples 



---

**Example: Using `promptlib` (alpha)**

You’ve got `zero-consult-clouds` CLI, with the new `promptlib` feature added.  
Here are five ways you might use it in practice:

---

1️⃣ **Browse available prompts**

`zero-consult-clouds promptlib browse`  
Opens a fast dialogue. Shows matching prompt files (UUID prefix, filename).  
You can scroll and select. First line of each file helps jog memory.

---

2️⃣ **Find a prompt using a keyword**

`zero-consult-clouds promptlib browse --filter "waterfall"`  
Filters list to filenames matching “waterfall”.  
Lets you jump quickly to the right prompt family.

---

3️⃣ **Copy prompt path**

Inside dialogue: press `c` on a selected prompt.  
Copies full path of the markdown file to clipboard.  
Use it anywhere — Obsidian, editor, other tools.

---

4️⃣ **Simple stdout output**

`zero-consult-clouds promptlib cat 39263c66`  
Prints full content of that prompt to stdout.  
Pipe it, edit it, send it anywhere.

---

5️⃣ **See total prompts**

`zero-consult-clouds promptlib stats`  
Outputs:  
“147 promptlib files found in archive /l/obs-chaotic”  
Helps track growth of the library.

---

## terminal visual 

Here is the next doc example, same voice, showing what happens when you run `zero-consult-clouds promptlib browse` — a pretend "Codex already built this" description:

---

**Interactive prompt: `promptlib browse`**

Run:  
`zero-consult-clouds promptlib browse`

---

You see something like this:

```
promptlib archive: /l/obs-chaotic  
total: 147 prompts  

╭────────────────────────────────────────────╮  
│ SEARCH: waterfall                          │  
│                                            │  
│ 39263c66-waterfall-planning.md              │  
│     * AI-assisted waterfall planning        │  
│                                            │  
│ 28472b19-waterfall-2.0-notes.md             │  
│     * Notes toward waterfall 2.0            │  
│                                            │  
│ 18219ffa-agentic-waterfall-iteration.md     │  
│     * Iterative planning with agents        │  
│                                            │  
╰────────────────────────────────────────────╯  

UP/DOWN to scroll.  
ENTER to select.  
`c` to copy path.  
`q` to quit.  
```

---

Notes:

- The first line of each file is shown (if available).
    
- If you type in SEARCH, it does live filter.
    
- Minimal — fast and text-friendly.
    
- Works well in your terminal — no GUI dependency.
    

---

# prompt 


Here is the updated Codex prompt — incorporating everything so far, shaped for first implementation:

---

**PRODUCT**

You are Codex, updating an existing CLI codebase.  
You are implementing a _promptlib manager_ — first alpha version.

Core behavior:

- Prompt files are markdown files.
    
- Each file contains a full UUID in its content: `39263c66-ded0-4261-9805-0acacd1814d1`.
    
- Filenames are prefixed with the short UUID: `39263c66-something.md`.
    
- Files that include `promptlib` in the filename are treated as prompts.
    
- Prompts live in an archive folder (example: `/l/obs-chaotic`).
    

You are adding these features:

1. CLI command: `zero-consult-clouds promptlib browse`
    
    - Opens an interactive dialogue.
        
    - Shows matching prompt files.
        
    - Shows first line of file (if any).
        
    - Supports SEARCH filter (live substring).
        
    - Allows scrolling, selecting, copying path.
        
    - Example UI given below.
        
2. Config update:
    
    - Add config var for promptlib archive path.
        
    - Update CLI to generate default config with this var.
        
    - Ensure CLI reads this var when loading promptlib.
        
3. CLI command: `zero-consult-clouds promptlib cat <uuid>`
    
    - Outputs full prompt content to stdout.
        
4. CLI command: `zero-consult-clouds promptlib stats`
    
    - Outputs total prompt count + archive path.
        

Example:  
When running `promptlib browse`, user sees:

```
promptlib archive: /l/obs-chaotic  
total: 147 prompts  

╭────────────────────────────────────────────╮  
│ SEARCH: waterfall                          │  
│                                            │  
│ 39263c66-waterfall-planning.md              │  
│     * AI-assisted waterfall planning        │  
│                                            │  
│ 28472b19-waterfall-2.0-notes.md             │  
│     * Notes toward waterfall 2.0            │  
│                                            │  
│ 18219ffa-agentic-waterfall-iteration.md     │  
│     * Iterative planning with agents        │  
│                                            │  
╰────────────────────────────────────────────╯  

UP/DOWN to scroll.  
ENTER to select.  
`c` to copy path.  
`q` to quit.  
```

Assume you are working in an existing CLI — do not rewrite unrelated parts.  
This is the first alpha — focus on simple and usable.  
Code should be readable, maintainable, ready to evolve.

END_PRODUCT

---

--- okay this prompt isn't quite worded correctly but I think you'll get it. implement an alpha version of `zero-consult-clouds promptlib` as described here (with an eye toward possible/likely future updates). 

***