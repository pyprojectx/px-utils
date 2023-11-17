import re
import shutil
from pathlib import Path

glob_regex = re.compile(r"[*?[]")


def _split_glob(path):
    parts = Path(path).parts
    glob_index = next((i for i, part in enumerate(parts) if glob_regex.search(part)), None)
    if glob_index is None:
        return Path(path), None
    return Path().joinpath(*parts[:glob_index]), "/".join(parts[glob_index:])


def mkdirs(directory):
    Path(directory).mkdir(exist_ok=True, parents=True)


def copytree(src, dst):
    src_path, glob = _split_glob(src)
    if glob:
        dst_path = Path(dst)
        for file in src_path.glob(glob):
            if file.is_file():
                d = dst_path.joinpath(file.relative_to(src_path))
                d.parent.mkdir(exist_ok=True, parents=True)
                shutil.copy2(file, d)
    else:
        shutil.copytree(src, dst, dirs_exist_ok=True)


def rmtree(path):
    p, glob = _split_glob(path)
    if p.absolute() == p.absolute().parent:
        raise ValueError(f"Refusing to delete {path} as it seems to be a filesystem root")

    if glob:
        for file in p.glob(glob):
            if file.is_file():
                file.unlink()
    elif p.exists():
        if p.is_file():
            p.unlink()
        else:
            shutil.rmtree(path)


def movetree(src, dst):
    src_path, glob = _split_glob(src)
    if glob:
        dst_path = Path(dst)
        for file in src_path.glob(glob):
            if file.is_file():
                d = dst_path.joinpath(file.relative_to(src_path))
                d.parent.mkdir(exist_ok=True, parents=True)
                shutil.move(file, d)
    else:
        shutil.move(src, dst)
