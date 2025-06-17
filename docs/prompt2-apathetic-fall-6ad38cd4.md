# prompt2 - bugfix apathetic-fall 6ad38cd4

random codename: apathetic-fall 6ad38cd4

#prompt 

***

```

/l/tmp via 🅒 zero 
❯ ls

/l/tmp via 🅒 zero 
❯ zero-ai-dev-framework newproject --new -f /l/tmp/zero-nutr-club -n "zero_nutr_club"
Traceback (most recent call last):
  File "/home/zero/miniconda3/envs/zero/bin/zero-ai-dev-framework", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/zero/code-repos/zero-ai-assisted-dev-project-template/consult-clouds/cli.py", line 47, in main
    duplicate_project(Path(args.filepath), args.project_name)
  File "/home/zero/code-repos/zero-ai-assisted-dev-project-template/consult-clouds/main.py", line 54, in duplicate_project
    cli_link.unlink()
  File "/home/zero/miniconda3/envs/zero/lib/python3.11/pathlib.py", line 1147, in unlink
    os.unlink(self)
IsADirectoryError: [Errno 21] Is a directory: '/l/tmp/zero-nutr-club/cli.py'

/l/tmp via 🅒 zero 
❯ zero-ai-dev-framework dev --new-doc
/home/zero/code-repos/zero-ai-assisted-dev-project-template/docs/unnamed-apathetic-fall-6ad38cd4.md

/l/tmp via 🅒 zero 
❯ 





```

I get this. 

also, there is this : 

```

/l/tmp/zero-nutr-club is 📦 v0.1.0 via 🐍 v3.11.8 via 🅒 zero 
❯ pip install -e . 
Obtaining file:///home/zero/Downloads/zero-nutr-club
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Preparing editable metadata (pyproject.toml) ... done
Requirement already satisfied: GitPython in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from zero-ai-dev-framework==0.1.0) (3.1.44)
Requirement already satisfied: jinja2>=3.0 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from zero-ai-dev-framework==0.1.0) (3.1.5)
Requirement already satisfied: codenamize in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from zero-ai-dev-framework==0.1.0) (1.2.3)
Requirement already satisfied: pytest in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from zero-ai-dev-framework==0.1.0) (8.4.0)
Requirement already satisfied: pandas in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from zero-ai-dev-framework==0.1.0) (2.2.3)
Requirement already satisfied: matplotlib in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from zero-ai-dev-framework==0.1.0) (3.10.0)
Requirement already satisfied: MarkupSafe>=2.0 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from jinja2>=3.0->zero-ai-dev-framework==0.1.0) (3.0.2)
Requirement already satisfied: six in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from codenamize->zero-ai-dev-framework==0.1.0) (1.16.0)
Requirement already satisfied: wheel in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from codenamize->zero-ai-dev-framework==0.1.0) (0.45.1)
Requirement already satisfied: gitdb<5,>=4.0.1 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from GitPython->zero-ai-dev-framework==0.1.0) (4.0.12)
Requirement already satisfied: contourpy>=1.0.1 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from matplotlib->zero-ai-dev-framework==0.1.0) (1.3.1)
Requirement already satisfied: cycler>=0.10 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from matplotlib->zero-ai-dev-framework==0.1.0) (0.12.1)
Requirement already satisfied: fonttools>=4.22.0 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from matplotlib->zero-ai-dev-framework==0.1.0) (4.56.0)
Requirement already satisfied: kiwisolver>=1.3.1 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from matplotlib->zero-ai-dev-framework==0.1.0) (1.4.8)
Requirement already satisfied: numpy>=1.23 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from matplotlib->zero-ai-dev-framework==0.1.0) (2.0.1)
Requirement already satisfied: packaging>=20.0 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from matplotlib->zero-ai-dev-framework==0.1.0) (24.2)
Requirement already satisfied: pillow>=8 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from matplotlib->zero-ai-dev-framework==0.1.0) (11.1.0)
Requirement already satisfied: pyparsing>=2.3.1 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from matplotlib->zero-ai-dev-framework==0.1.0) (3.2.1)
Requirement already satisfied: python-dateutil>=2.7 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from matplotlib->zero-ai-dev-framework==0.1.0) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from pandas->zero-ai-dev-framework==0.1.0) (2024.1)
Requirement already satisfied: tzdata>=2022.7 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from pandas->zero-ai-dev-framework==0.1.0) (2023.3)
Requirement already satisfied: iniconfig>=1 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from pytest->zero-ai-dev-framework==0.1.0) (2.1.0)
Requirement already satisfied: pluggy<2,>=1.5 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from pytest->zero-ai-dev-framework==0.1.0) (1.6.0)
Requirement already satisfied: pygments>=2.7.2 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from pytest->zero-ai-dev-framework==0.1.0) (2.19.1)
Requirement already satisfied: smmap<6,>=3.0.1 in /home/zero/miniconda3/envs/zero/lib/python3.11/site-packages (from gitdb<5,>=4.0.1->GitPython->zero-ai-dev-framework==0.1.0) (5.0.2)
Building wheels for collected packages: zero-ai-dev-framework
  Building editable for zero-ai-dev-framework (pyproject.toml) ... done
  Created wheel for zero-ai-dev-framework: filename=zero_ai_dev_framework-0.1.0-0.editable-py3-none-any.whl size=15762 sha256=6ab6fed0856ed6dea601a6c6a763a541062e933789ff0ece1728c48669a48e4b
  Stored in directory: /tmp/pip-ephem-wheel-cache-dt_syk4p/wheels/af/4c/33/fbc50e45d17f3066c1aea80ab8493cab0d2fc5ce355183bc9a
Successfully built zero-ai-dev-framework
Installing collected packages: zero-ai-dev-framework
  Attempting uninstall: zero-ai-dev-framework
    Found existing installation: zero-ai-dev-framework 0.1.0
    Uninstalling zero-ai-dev-framework-0.1.0:
      Successfully uninstalled zero-ai-dev-framework-0.1.0
Successfully installed zero-ai-dev-framework-0.1.0

/l/tmp/zero-nutr-club is 📦 v0.1.0 via 🐍 v3.11.8 via 🅒 zero took 2s 
❯ 

```

...it is not being renamed. 

running `zero-ai-dev-framework newproject --new -f /l/tmp/zero-nutr-club -n "zero_nutr_club"` should get me an installable cli tool named "zero_nutr_club" in the folder '/l/tmp/zero-nutr-club', this just being a random example name. but should be able to install w/ `pip install -e . ` and then run `zero-nutr-club -h`. note that whether or not to use "-" vs "`_`" depends on context, it is both zero_nutr_club and zero-nutr-club. 

apply fix. 
