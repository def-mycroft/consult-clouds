#  prompt1 - generate instance for new project

random codename: normal-associate 763211a8

#prompt 

***

see here: 

```prompt
 34     )                                                                           
 35                                                                                 
 36     args = parser.parse_args(argv)                                              
 37                                                                                 
 38     if args.command == "newproject":                                            
 39         if args.new_project:                                                    
 40             # new project                                                       
 41             # import code from consult-clouds.main to duplicate this      
 42             0                                                                   
 43     elif args.command == "dev":                                                 
 44         if args.update_toc:                                                     
 45             docs_tools.update_toc()                                             
 46         elif args.new_doc:                     
```

--- see where I have "new project" and "import code from consult-clouds.main to duplicate this". 

write a function in main which will duplicate this project and rename. 

so, implement `zero-ai-dev-framework newproject --new` , which will be used
like this: 

```
/l/tmp via 🅒 zero
❯ zero-ai-dev-framework newproject --new -f "project-codename-verdant-perception" -n "zero_verdant"


/l/tmp via 🅒 zero
❯ ls project-codename-verdant-perception/
cli.py  docs  LICENSE  logs  notebooks  pyproject.toml  README.md zero_verdant

/l/tmp via 🅒 zero
❯ tree project-codename-verdant-perception/
project-codename-verdant-perception/
├── cli.py -> zero_verdant/cli.py
├── docs
│   ├── 00projectanchor-template.md
│   ├── CONTENTS.md
│   ├── main_notes_adding_wiki_articles.md
│   ├── main_notes_as_a_human_how_to_code_with_codex.md
│   ├── main_notes_best_practices_coding_with_codex.md
│   ├── main_notes_business_value_research.md
│   ├── main_notes_checkpoint_prim_classes.md
│   ├── main_notes_codex_must_read_this_rules_for_codex.md
│   ├── main_notes_devplan.md
│   ├── main_notes_docstring_style_guide.md
│   ├── main_notes_for_codex_update_toc.md
│   ├── main_notes_styleguide_wiki_articles.md
│   ├── main_notes_wiki_article_creation_for_codex.md
│   ├── next-condition 0c44bdae.md
├── LICENSE
├── logs
├── notebooks
├── pyproject.toml
├── README.md
└── zero_verdant
    ├── assets
    │   └── new_doc_template.md.j2
    ├── cli.py
    ├── docs_tools.py
    ├── git_tools.py
    ├── helpers.py
    ├── __init__.py
    └── pandas_ext.py

6 directories, 27 files

/l/tmp via 🅒 zero
❯

```

... and note that we want all other ways in which the name of the thing is mentioned to be renamed. 
