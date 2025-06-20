# Rewrite Loop Primer

random codename: diligent-director 7da624a4-7713-4f82-a66c-84383dbf43e9

***

This project includes a feature called the **rewrite loop**. It is a command-line tool that helps you iteratively improve a piece of writing with the help of a language model. You start with a draft and a description of its purpose, and the program creates rewritten versions step by step.

### Why Use It

- Quickly refine a short article or blog post with guided feedback.
- Keep track of each iteration so you can compare improvements.
- Run in safe or dummy modes when you want to test the workflow without making API calls.

### What Happens Behind the Scenes

1. **Loading the Draft** – The `loops` command reads your input file. The first section is treated as the draft and anything after `***` is the context for the model.
2. **Summarizing the Purpose** – The tool sends the context to ChatGPT and prints a short bullet summary. You can then confirm whether the understanding is correct.
3. **Iterative Rewrites** – Each iteration sends your latest version along with any comments you provide. The response is written to a new `convo-YYYYMMDD-vN.md` file and bullet points outlining the changes appear in the terminal.
4. **Final Score** – After the last round, the tool asks ChatGPT to evaluate all versions and display a short report about which one best meets the stated goals.

The entire process is defined in `rewrite_loops.py`, while the command-line interface lives in `cli.py`. By default, the program interacts with the OpenAI API, but dummy and safe modes let you try it out without sending data anywhere.

### Example Workflow

Below is an abbreviated example that shows the basic flow using dummy mode so no API calls are made:

```text
$ cat draft.md
My first draft text.
***
Explain the purpose and audience.

$ zero-consult-clouds loops -f draft.md --dummy
Summarize the purpose and fitness goals in 5 bullet points:
- dummy response
Comments (or 'q' to quit):
dummy response
Another iteration? [y/N]
```

Each run saves a new `convo-YYYYMMDD-v1.md` file next to your draft and prints a short score report at the end.

