import os
from pathlib import Path

import pytest


@pytest.fixture()
def tmp_dir(tmp_path):
    r = tmp_path / "root"
    a = r / "subdir-a"
    ac = a / "subdir-ac"
    ac.mkdir(parents=True)
    b = r / "subdir-b"
    b.mkdir()
    (a / "a-file.txt").touch()
    (a / "a-picture.png").touch()
    (b / "b-file.txt").touch()
    (b / "b-picture.png").touch()
    (ac / "ac-file.txt").touch()
    (ac / "ac-picture.png").touch()
    cwd = Path.cwd()
    os.chdir(tmp_path.absolute())
    yield tmp_path
    os.chdir(cwd)
