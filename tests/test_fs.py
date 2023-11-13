from glob import glob

import pytest
from px_utils import fs


def test_is_glob():
    assert fs._is_glob("*.py")
    assert fs._is_glob("[a-z].py")
    assert fs._is_glob("foo.p?")
    assert not fs._is_glob("foo.py")


def test_mkdirs(tmp_path):
    path = tmp_path / "foo" / "bar"
    fs.mkdirs(path)
    assert path.exists()

    fs.mkdirs(path)  # should not raise an exception


def test_copytree_no_glob(tmp_dir):
    fs.copytree("root", "dest")
    assert glob("**/*.*", root_dir=tmp_dir / "root", recursive=True) == glob(
        "**/*.*", root_dir=tmp_dir / "dest", recursive=True
    )
    fs.copytree("root", "copy-of-root")  # should not raise an exception


@pytest.mark.parametrize(
    ("includes", "dest_files"),
    [
        ("**/*.txt", ["dest/subdir-a/a-file.txt", "dest/subdir-a/subdir-ac/ac-file.txt", "dest/subdir-b/b-file.txt"]),
        ("*a/*", ["dest/subdir-a/a-file.txt", "dest/subdir-a/a-picture.png"]),
        ("*a/**/*.png", ["dest/subdir-a/a-picture.png", "dest/subdir-a/subdir-ac/ac-picture.png"]),
    ],
)
def test_copytree_glob(tmp_dir, includes, dest_files):
    fs.copytree("root", "dest", includes=includes)
    assert glob("dest/**/*.*", root_dir=tmp_dir, recursive=True) == dest_files
    fs.copytree("root", "dest", includes=includes)  # should not raise an exception


def test_movetree_no_glob(tmp_dir):
    root_files = glob("**/*.*", root_dir=tmp_dir / "root", recursive=True)
    fs.movetree("root", "dest")
    assert glob("**/*.*", root_dir=tmp_dir / "dest", recursive=True) == root_files
    assert not glob("**/*.*", root_dir=tmp_dir / "root", recursive=True)


@pytest.mark.parametrize(
    ("includes", "dest_files"),
    [
        ("**/*.txt", ["dest/subdir-a/a-file.txt", "dest/subdir-a/subdir-ac/ac-file.txt", "dest/subdir-b/b-file.txt"]),
        ("*a/*", ["dest/subdir-a/a-file.txt", "dest/subdir-a/a-picture.png"]),
        ("*a/**/*.png", ["dest/subdir-a/a-picture.png", "dest/subdir-a/subdir-ac/ac-picture.png"]),
    ],
)
def test_movetree_glob(tmp_dir, includes, dest_files):
    fs.copytree("root", "dest", includes=includes)
    assert glob("dest/**/*.*", root_dir=tmp_dir, recursive=True) == dest_files
    assert not glob(f"root/{includes}", root_dir=tmp_dir / "root", recursive=True)


@pytest.mark.parametrize(
    ("path", "root_files"),
    [
        (
            "**/*.txt",
            ["root/subdir-a/a-picture.png", "root/subdir-a/subdir-ac/ac-picture.png", "root/subdir-b/b-picture.png"],
        ),
        (
            "*a/*",
            [
                "root/subdir-a/a-file.txt",
                "root/subdir-a/a-picture.png",
                "root/subdir-a/subdir-ac/ac-file.txt",
                "root/subdir-a/subdir-ac/ac-picture.png",
                "root/subdir-b/b-picture.png",
                "root/subdir-b/b-file.txt",
            ],
        ),
        (
            "*a/**/*.png",
            [
                "root/subdir-a/a-file.txt",
                "root/subdir-a/a-picture.png",
                "root/subdir-a/subdir-ac/ac-file.txt",
                "root/subdir-a/subdir-ac/ac-picture.png",
                "root/subdir-b/b-picture.png",
                "root/subdir-b/b-file.txt",
            ],
        ),
    ],
)
def test_rmtree(tmp_dir, path, root_files):
    fs.rmtree(path)
    assert glob("**/*.*", root_dir=tmp_dir, recursive=True) == root_files
    fs.rmtree(path)  # should not raise an exception
