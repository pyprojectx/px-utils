import os
from pathlib import Path

# extract version from tag
RELEASE_VERSION = os.environ["GITHUB_REF_NAME"]

# cleanup old files
Path(".changelog.md").unlink(missing_ok=True)

# replace __version__ in wrapper and pyproject.toml
pyproject = Path("pyproject.toml")
pyproject.write_text(pyproject.read_text().replace("1.0.0.dev", RELEASE_VERSION))

# extract the first change log from CHANGELOG.md
with Path("CHANGELOG.md").open() as changelog, Path(".changelog.md").open("w") as out:
    fist_header = False
    for line in changelog:
        if not fist_header:
            if line.startswith("###"):
                fist_header = True
            else:
                continue
        if fist_header and line.startswith("Release"):
            break
        out.write(line)
