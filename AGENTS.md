# AGENTS.md

Guidance for coding agents working in this repository.

## Project

`px-utils` publishes four cross-platform file-operation CLIs (`pxmkdirs`, `pxcp`, `pxmv`, `pxrm`) intended to replace
`mkdir -p`/`cp`/`mv`/`rm` in build scripts so those scripts work identically on Windows and *nix. It is designed to be
used from [pyprojectx](https://pyprojectx.github.io/) aliases, and it dogfoods pyprojectx for its own build.

## Commands

**Everything goes through `./pw`.** Never invoke `uv`, `pytest`, or `ruff` from the system
PATH — a system copy is a different version than the one this project pins, and it runs outside the
tool context. Prefix every `uv` call with the wrapper (`./pw uv sync`, `./pw uv pip list`): `uv` is
a requirement of the `main` tool context, so `./pw uv …` runs the project's own uv. `pytest`, and `ruff`
are reached through their aliases below, or via `./pw uv run <tool>`.

The wrapper is `pw.bat` on Windows and `python pw <cmd>` anywhere; it bootstraps its own tool venvs
in `.pyprojectx/` — do not create a venv or `pip install` manually.

Aliases are defined in `[tool.pyprojectx.aliases]`; in addition, every `bin/*.py` file is auto-discovered as a
pyprojectx *script* and runs in the `main` tool context (`./pw cli-help`, `./pw prep-release`). Both show up in
`./pw --info`.

```
./pw install       # uv sync (creates .venv from uv.lock)
./pw test          # uv run pytest tests
./pw lint          # ruff check
./pw format        # ruff format + ruff check --select I --fix (import sorting)
./pw check         # lint + test
./pw build         # install + check + uv build + regenerate README CLI section
./pw clean         # remove .venv .pytest_cache dist .ruff_cache
./pw update        # uv lock
```

Run a single test: `./pw uv run pytest tests/test_fs.py::test_mkdirs` (or `-k <pattern>`).
Run a CLI against the working tree: `./pw uv run pxcp "src/**/*.py" build`.

`prek` (installed automatically by the `post-install = "prek install"` hook of the `main` tool context) runs
`pw format` and `pw lint` on every commit.

## Architecture

Two layers, ~150 lines total:

- `src/px_utils/fs.py` — the logic. Pure functions over `pathlib`/`shutil`, no argparse, no `sys.exit`.
- `src/px_utils/cli.py` — one argparse entry point per command, wired up in `[project.scripts]` in `pyproject.toml`.
  `cp` and `mv` share `_copy(move=...)`; the argparse `description=` strings here are the source of truth for the
  user-facing docs (see below).

The central mechanism is `fs._split_glob(path)`: it walks the path parts, finds the first one containing `* ? [`, and
returns `(base_dir, glob_pattern)` — or `(path, None)` when there is no glob. Everything else follows from that split:

- **Globs are expanded by the tool, not the shell.** That is why every help string insists globs be quoted on *nix, and
  why behaviour is identical on Windows.
- **Directory structure is preserved relative to the glob base.** Copy/move place each match at
  `dst / file.relative_to(base_dir)`, creating parents as needed. `pxcp "root/**/*.txt" dest` therefore mirrors the tree
  under `root` into `dest`, not a flat dump.
- **Glob branches only act on files**; directory matches are skipped (`if file.is_file()`). The no-glob branch delegates
  to `shutil.copytree(dirs_exist_ok=True)` / `shutil.move` / `shutil.rmtree`, so whole directories move as a unit.
- `fs.rmtree` refuses a path whose absolute form is its own parent (a filesystem root) and is a silent no-op on
  missing paths.

Tests (`tests/test_fs.py`) drive `fs` directly, not the CLIs. The `tmp_dir` fixture in `conftest.py` builds a fixed
sample tree and `chdir`s into it, so tests use relative paths throughout and each case asserts on the exact set of
resulting files.

## Conventions

- **`requires-python = ">=3.9"`** and CI builds on 3.9–3.14 × Ubuntu/Windows. No `match` statement and no PEP 604
  `X | Y` unions (both 3.10+). Type annotations are absent by design (ruff's `ANN` rules are disabled).
- Ruff with `select = ["ALL"]`, line length 120. Check `[tool.ruff.lint.ignore]` in `pyproject.toml` before adding
  `# noqa`.
- **The `<!-- START-CLI -->` … `<!-- END-CLI -->` block in README.md is generated.** Never edit it by hand; change the
  argparse text in `cli.py` and regenerate with `./pw cli-help`, which runs each script's `--help` and splices the
  output in. `./pw build` does this as its last step. Use the script, not `./pw uv run python bin/cli-help.py` —
  `tomlkit` is a `main` requirement and is *not* in the project `.venv`.
- **Version is a placeholder.** `pyproject.toml` stays at `1.0.0.dev` on `main`; `bin/prep-release.py` substitutes the
  git tag name into it during the release workflow and extracts the newest `CHANGELOG.md` entry into `.changelog.md`
  for the GitHub release body. Add a `Release vX.Y.Z (date)` section to `CHANGELOG.md` before tagging.
- Releases fire on tags matching `[0-9]+.[0-9]+.[0-9]+*` (`.github/workflows/release.yml`) and publish to PyPI.
