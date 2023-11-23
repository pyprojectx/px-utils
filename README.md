![pyprojectx](px.png)

# Px-utils

Cross-platform build utilities for python projects, especially useful for projects using [pyprojectx](https://pyprojectx.github.io/)

Currently limited to file operations.

## Installation

```
pip install px-utils
```

Or using Pyprojectx:

```toml
[tool.pyprojectx]
px-utils= "px-utils"

[tool.pyprojectx.aliases]
clean = "@px-utils: prm build dist .pytest_cache .coverage"
```

## File operations

<!-- START-CLI -->
## pxmkdirs
usage: pxmkdirs [-h] directories [directories ...]

Create a directory and any missing parent directories.

positional arguments:
  directories  The director(y)(ies) to create.

options:
  -h, --help   show this help message and exit

## pxcp
usage: pxcp [-h] source_files [source_files ...] destination

Copy source files to a destination directory. The source can be multiple files
or globs. Files are copied preserving directory structure.

positional arguments:
  source_files  The files to copy. Can be multiple files/globs. IMPORTANT:
                when using globs, they must be quoted in order to prevent
                expansion by *nix shells!
  destination   The destination directory.

options:
  -h, --help    show this help message and exit

## pxmv
usage: pxmv [-h] source_files [source_files ...] destination

Move source files to a destination directory. The source can be multiple files
or globs. Files are moved preserving directory structure.

positional arguments:
  source_files  The files to move. Can be multiple files/globs. IMPORTANT:
                when using globs, they must be quoted in order to prevent
                expansion by *nix shells!
  destination   The destination directory.

options:
  -h, --help    show this help message and exit

## pxrm
usage: pxrm [-h] files [files ...]

Delete files or globs.

positional arguments:
  files       The files to delete. Can be multiple files/globs. IMPORTANT:
              when using globs, they must be quoted in order to prevent
              expansion by *nix shells!

options:
  -h, --help  show this help message and exit

<!-- END-CLI -->
