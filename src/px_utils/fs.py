import re
import shutil
from glob import iglob
from pathlib import Path

glob_regex = re.compile(r"[*?[]")


def _is_glob(path):
    return glob_regex.search(str(path))


def mkdirs(path):
    Path(path).mkdir(exist_ok=True, parents=True)


def copytree(src, dst, includes=None):
    if includes:
        src_path = Path(src)
        for file in iglob(includes, root_dir=src, recursive=True):
            file_path = src_path / file
            if file_path.is_file():
                d = Path(dst) / file
                d.parent.mkdir(exist_ok=True, parents=True)
                shutil.copy2(file_path, d)
    else:
        shutil.copytree(src, dst, dirs_exist_ok=True)


def rmtree(path):
    p = Path(path)
    if p == p.parent:
        raise ValueError(f"Refusing to delete {path} as it seems to be a filesystem root")

    if _is_glob(path):
        for file in iglob(path, recursive=True):
            Path(file).unlink()
    else:
        shutil.rmtree(path)


def movetree(src, dst, includes=None):
    if includes:
        src_path = Path(src)
        for file in iglob(includes, root_dir=src, recursive=True):
            file_path = src_path / file
            if file_path.is_file():
                d = Path(dst) / file
                d.parent.mkdir(exist_ok=True, parents=True)
                shutil.move(file_path, d)
    else:
        shutil.move(src, dst)
