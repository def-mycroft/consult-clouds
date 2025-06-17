# prompt1 - implement context lib

random codename: glib-manner 53a53225

#prompt 

***


# part 1

right now we have: 

`zero-consult-clouds convo -f /l/tmp/input.md -o /l/tmp/output.md`

item 1 - whenever `convo` is used to send text to chatgpt like this, output to a default dir that is specified in the project config. if this path isn't listed, require that the user provide it. 

so, if I have `/l/tmp` listed in my config as the default output dir, then I can just run: 

`zero-consult-clouds convo -f /l/tmp/input.md`

...in order to do the same thing i.e. outcome will be written to `/l/tmp/output.md` 


this should be setup when setting up config via cli. 


# part 2

also, after doing part 1, write a function which takes the json conversation object (the full output of the resopnse when sending a message), and writes out a markdown document at the same output dir (same place output.md is written). this function will summarize the conversation and allow user to browse it. it should have headings, a toc and it should progress with most recent on top. h1 headings "Prompt" are what the user sent, h2 headings "Response" follow each of those and show the response from teh chatbot. 

then, by default running `convo` w/ `-f` will write this document after the call, including the response from the chatbot. so should be able to open up some file like `/l/tmp/history.md` and get this clickable md doc that summarizes what happened. 

include a switch on `convo` `--disable-history-write` which neglects to write history.md

# part 3

now...want to have 

```
zero-consult-clouds convo -f /l/tmp/input.md --promptlib-pretext "fb92cfa1"
```

also require that user setup a path that points toward a "prompt lib dir", which is where the promptlib is stored. 

promptlib is a dir that has files. files have uuids in filenames, or at least partial uuids. 

infer what you're supposed to do by generalizing rom this example: 

    ...that uuid, "fb92cfa1". if you find exactly one file in promptlib dir with that substring in the filename, the load text from that file. if you don't find exactly one matching that "fb92cfa1" uuid substring, raise Exception. 
    then, prior to sending contents of `input.md` via api, prepend contents of fb92cfa1 to the prompt. 
    so, if user passed fb92cfa1 as --promptlib-pretext, and if `input.md` contains "here are the instructions" in one line, then what will be sent to the chatbot will be "{{ contents of fb92cfa1 }} \n***\nhere are the instructions"


... basically, passing --prompt-lib pretext looks up a text file in the promptlib and simply prepends tha ttext to whatever is otherwise being sent to chatgpt. 

also, can pass `--promptlib-pretext` multiple times with different uuid substrings to prepend multiple pretexxsts. 


