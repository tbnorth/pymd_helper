"""
update_md.py - insert files into markdown

Recursively searches for markdown (.md) files and updates in place when it
finds a <!-- --> comment matching its expected command structure.

Currently only supports
<!-- insert,src=./some/path.sh,type=code,syntax=shell -->
```shell
[./some/path.sh inserted/update here]
```

Terry N. Brown terrynbrown@gmail.com Wed 03 Jun 2020 08:44:37 PM CDT
"""

import os
import re
from pathlib import Path

# pattern used to recognize commands, basically
# <!-- cmd_name,arg1=val1,arg2=val2 -->
PATTERN = r"^<!-- \|\w+,?(\w+[^,]+,?)* -->"


def recurse(path=None):
    """Recursively search for markdown files and process them"""
    todo = [path]
    while todo:
        path = todo.pop(0)
        for dirent in os.scandir(path):
            if dirent.is_dir():
                todo.append(dirent.path)
            elif Path(dirent).suffix.lower() == ".md":
                proc(dirent)


def proc_documentation(args, old, line_i, new):
    args["type"] = "documentation"
    args["src"] = os.path.join(os.path.dirname(__file__), "documentation.txt")
    return proc_insert(args, old, line_i, new)


def proc_insert(args, old, line_i, new):
    # Insertion types.  `delim` are the new delimiters we put in.  `fences` are
    # the old delimiters we skip over.
    types = {
        "code": {
            "delim": ["{addpath}```{syntax}\n", "```\n"],
            "fences": [r"(^<div class='addpath|^```\w)", r"```\s*$"],
        },
        "comment": {
            "delim": ["<!-- ", "\n     -->\n"],
            "fences": ["^<!--", "-->"],
        },
        "documentation": {"delim": ["", ""], "fences": ["^<!--", "-->"]},
    }
    args.setdefault("type", "code")
    args.setdefault("syntax", "text")
    # read the documentation documentation, in this file's folder
    if args.get("addpath"):
        # this really only makes sense / works for `code` type insertions
        # NOTE: needs \n\n for GitHub to recognize ``` properly
        args["addpath"] = (
            f"""<div class='addpath'>(<a href="{args['src']}">"""
            f"""<i>{args['src']}</i></a>)</div>\n\n"""
        )
    else:
        args["addpath"] = ""
    new.append(types[args["type"]]["delim"][0].format_map(args))
    with open(os.path.join(os.path.dirname(args["dirent"]), args["src"])) as src:
        new.extend(src)
    new.append(types[args["type"]]["delim"][1].format_map(args))
    fences = [re.compile(i) for i in types[args["type"]]["fences"]]
    if fences[0].search(old[line_i]):
        while fences:  # drop lines fenced lines in src
            if fences[0].search(old[line_i]):
                del fences[0]
            line_i += 1
    return line_i


def get_link(text):
    """Turn a markdown headline in to a link, # Hello World -> hello-world"""
    return "".join(
        i if i in "-_" or ("a" <= i <= "z") else ""
        for i in text.lower().replace(" ", "-")
    )


def proc_toc(args, old, line_i, new):
    in_code = False
    for line in old[line_i:]:
        if line[:3] == "```":
            in_code = not in_code
        if not in_code and line.startswith("#"):
            indent = min(5, len(line) - len(line.lstrip("#")) - 1)
            leader = "  " * indent + " - "
            text = line.lstrip(" #").strip()
            link = get_link(text)
            new.append(f"{leader}[{text}](#{link})\n")
    while old[line_i].lstrip().startswith("- "):
        line_i += 1

    return line_i


def proc(dirent):
    """Process one markdown file"""
    pattern = re.compile(PATTERN)
    with open(dirent) as md_src:
        old = list(md_src)
    new = []  # accumulated lines with insertions etc.
    hits = 0  # number of command comments seen
    line_i = 0
    while line_i < len(old):
        line = old[line_i]
        line_i += 1
        new.append(line)
        if pattern.search(line):  # found a command comment
            if hits == 0:  # first one in this file
                print(dirent.path)
            hits += 1
            print(line.strip())
            cmd, *args = line[6:-5].split(",")
            args = dict(i.split("=") if "=" in i else (i, True) for i in args)
            args["dirent"] = dirent  # needed for insert paths
            line_i = globals()[f"proc_{cmd}"](args, old, line_i, new)

    # for comparison, convert to str so ['', 'a'] and ['a', ''] match etc.
    old = "".join(old)
    new = "".join(new)
    if hits and old == new:
        print("No change")  # no output if no command comments seen (hits == 0)
    elif hits:
        print("CHANGED")
        with open(dirent, "w") as out:  # write updated file in place
            out.write(new)


if __name__ == "__main__":
    recurse()
