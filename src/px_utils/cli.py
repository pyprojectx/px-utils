import argparse
import sys
from pathlib import Path

from px_utils import fs

GLOB_MSG = (
    "Can be multiple files/globs. "
    "IMPORTANT: when using globs, they must be quoted in order to prevent expansion by *nix shells!"
)


def mkdirs():
    parser = argparse.ArgumentParser(description="Create a directory and any missing parent directories.")
    parser.add_argument("directories", nargs="+", help="The director(y)(ies) to create.")
    for directory in parser.parse_args(sys.argv[1:]).directories:
        fs.mkdirs(directory)


def cp():
    _copy(move=False)


def rm():
    parser = argparse.ArgumentParser(description="Delete files or globs.")
    parser.add_argument(
        "files",
        nargs="+",
        help=f"The files to delete. {GLOB_MSG}",
    )
    args = parser.parse_args(sys.argv[1:])
    for file in args.files:
        fs.rmtree(file)


def mv():
    _copy(move=True)


def _copy(move):
    name = "move" if move else "copy"
    verb = "moved" if move else "copied"
    parser = argparse.ArgumentParser(
        description=f"{name.capitalize()} source files to a destination directory. "
        f"The source can be multiple files or globs. Files are {verb} preserving directory structure."
    )
    parser.add_argument(
        "source_files",
        nargs="+",
        help=f"The files to {name}. {GLOB_MSG}",
    )
    parser.add_argument("destination", nargs=1, help="The destination directory.")
    args = parser.parse_args(sys.argv[1:])
    destination = args.destination[0]
    destination_path = Path(destination)
    if destination_path.exists() and not Path(destination).is_dir():
        print(f"Destination '{args.destination[0]}' is not a directory!\n", file=sys.stderr)
        sys.exit(1)
    for source in args.source_files:
        if move:
            fs.movetree(source, destination)
        else:
            fs.copytree(source, destination)
