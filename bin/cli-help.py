#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path

import tomlkit

project_dir = Path(__file__).parent.parent
toml_path = project_dir / "pyproject.toml"
readme_file = project_dir / "README.md"

help_text = []
with toml_path.open("rb") as f:
    toml_dict = tomlkit.load(f)
    for script in toml_dict["project"]["scripts"]:
        help_text.append(f"## {script}")
        p = subprocess.run(f"{project_dir}/pw uv run {script} --help", shell=True, capture_output=True, check=True)
        help_text.append(p.stdout.decode("utf-8"))

with readme_file.open() as r:
    readme = r.read()
    global_regex = re.compile(r"<!-- START-CLI -->.*<!-- END-CLI -->", re.DOTALL)
    readme = global_regex.sub("<!-- START-CLI -->\n" + "\n".join(help_text) + "\n<!-- END-CLI -->", readme)
with readme_file.open("w") as r:
    r.write(readme)

print("Updated README.md with CLI help")
