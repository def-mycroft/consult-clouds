# Wiki Article Creation Instructions for Codex

#process-notes

random codename: humorous-emphasis ea38febd

***

for codex: when creating a new wiki article, use func `helpers.codename` to generate a codename and format the article similr to this one, i.e. 

```
# Title Case Article Title
random codename: <codename that you'll generate>

***

<article content> 
```


also, whenever you update or create any `md` file in "docs/", the last thing before commit you should do is run `zcc dev --update-doc` or the code equivalent (i.e. use the code to update CONTENTS.md you don't edit).

