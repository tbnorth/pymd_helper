# pymd_helper

<!-- |documentation -->
<!-- Please see https://github.com/tbnorth/pymd_helper for instructions on
     updating this projects markdown files.  `pymd_helper` is used to
     insert/update files into markdown documentation, generate tables
     of contents, etc.
-->

Python GitHub Markdown helper - include files in markdown, table of contents, etc.

<!-- |toc -->
   - [Overview](#overview)
   - [Available commands](#available-commands)
     - [Insert a file `insert`](#insert-a-file-insert)
     - [Insert a table of contents `toc`](#insert-a-table-of-contents-toc)
     - [Insert documentation about this documentation system `documentation`](#insert-documentation-about-this-documentation-system-documentation)
   - [How it works](#how-it-works)
   - [Similar tools](#similar-tools)

## Overview

`pymd_helper` uses specially formatted markdown comments (`<!-- |cmd,args...
-->`) to enrich markdown documentation in git repositories (GitHub, etc.).
`pymd_helper` can insert files into code blocks to keep documentation in sync.
with actual code, and generate a table of contents.

## Available commands

### Insert a file `insert`

```
    <!-- |insert,src=examples/script.sh,syntax=shell,addpath -->
```
will insert the contents of the file `script.sh` in a markdown code block with
`shell` syntax highlighting:
<!-- |insert,src=examples/script.sh,syntax=shell,addpath -->
<div class='addpath'>(<a href="examples/script.sh"><i>examples/script.sh</i></a>)</div>

```shell
# this isn't a real script
ARG1=$1
cp $ARG1 /dev/null
echo "Copy complete"
```

The presence of the `addpath` parameter controls the presence of the
`(examples/script.sh)` link
preceding the code block.  `type=comment` can be added to the `|insert` command
line to insert a `<!-- -->` comment block rather than a code block.

### Insert a table of contents `toc`

```
   <!-- |toc -->
```
will generate a table of contents for the markdown headings (#, ##, …) in the
**remainder** of the markdown file.

### Insert documentation about this documentation system `documentation`

```
    <!-- |documentation -->
```
will insert the following comment in your markdown.

<!-- |insert,src=pymd_helper/documentation.txt,type=code,syntax=html -->
```html
<!-- Please see https://github.com/tbnorth/pymd_helper for instructions on
     updating this projects markdown files.  `pymd_helper` is used to
     insert/update files into markdown documentation, generate tables
     of contents, etc.
-->
```
This comment is not visible to people viewing the repository's rendered
markdown, but provides information for people updating the markdown directly.

## How it works

## Similar tools
