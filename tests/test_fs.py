from pathlib import Path

import pytest
from px_utils import fs


def test_split_glob():
    assert fs._split_glob("*.py") == (Path(), "*.py")
    assert fs._split_glob("foo/bar/[a-z].py") == (Path("foo/bar"), "[a-z].py")
    assert fs._split_glob("foo/foo.p?/bar") == (Path("foo"), str(Path("foo.p?/bar")))
    assert fs._split_glob("foo.py") == (Path("foo.py"), None)


def test_mkdirs(tmp_path):
    path = tmp_path / "foo" / "bar"
    fs.mkdirs(path)
    assert path.exists()
    fs.mkdirs(path)  # should not raise an exception


@pytest.mark.usefixtures("tmp_dir")
def test_copytree_no_glob():
    fs.copytree("root", "dest")
    assert set(Path().glob("dest/**/*.*")) == {
        Path("dest/subdir-a/a-file.txt"),
        Path("dest/subdir-a/a-picture.png"),
        Path("dest/subdir-a/subdir-ac/ac-file.txt"),
        Path("dest/subdir-a/subdir-ac/ac-picture.png"),
        Path("dest/subdir-b/b-file.txt"),
        Path("dest/subdir-b/b-picture.png"),
    }
    fs.copytree("root", "copy-of-root")  # should not raise an exception


@pytest.mark.usefixtures("tmp_dir")
@pytest.mark.parametrize(
    ("src", "dest_files"),
    [
        (
            "**/*.txt",
            {
                "dest/root/subdir-a/a-file.txt",
                "dest/root/subdir-a/subdir-ac/ac-file.txt",
                "dest/root/subdir-b/b-file.txt",
            },
        ),
        (
            "root/**/*.txt",
            {
                "dest/subdir-a/a-file.txt",
                "dest/subdir-a/subdir-ac/ac-file.txt",
                "dest/subdir-b/b-file.txt",
            },
        ),
        ("root/*a/*", {"dest/subdir-a/a-file.txt", "dest/subdir-a/a-picture.png"}),
        ("root/*a/**/*.png", {"dest/subdir-a/a-picture.png", "dest/subdir-a/subdir-ac/ac-picture.png"}),
        ("root/subdir-b/*.png", {"dest/b-picture.png"}),
    ],
)
def test_copytree_glob(src, dest_files):
    fs.copytree(src, "dest")
    assert set(Path().glob("dest/**/*.*")) == {Path(p) for p in dest_files}
    fs.copytree(src, "dest")  # should not raise an exception


@pytest.mark.usefixtures("tmp_dir")
def test_movetree_no_glob():
    fs.movetree("root", "dest")
    assert set(Path().glob("dest/**/*.*")) == {
        Path("dest/subdir-a/a-file.txt"),
        Path("dest/subdir-a/a-picture.png"),
        Path("dest/subdir-a/subdir-ac/ac-file.txt"),
        Path("dest/subdir-a/subdir-ac/ac-picture.png"),
        Path("dest/subdir-b/b-file.txt"),
        Path("dest/subdir-b/b-picture.png"),
    }
    assert not Path("root").exists()


@pytest.mark.usefixtures("tmp_dir")
@pytest.mark.parametrize(
    ("src", "dest_files"),
    [
        (
            "**/*.txt",
            {
                "dest/root/subdir-a/a-file.txt",
                "dest/root/subdir-a/subdir-ac/ac-file.txt",
                "dest/root/subdir-b/b-file.txt",
            },
        ),
        ("root/*a/*", {"dest/subdir-a/a-file.txt", "dest/subdir-a/a-picture.png"}),
        ("root/*a/**/*.png", {"dest/subdir-a/a-picture.png", "dest/subdir-a/subdir-ac/ac-picture.png"}),
    ],
)
def test_movetree_glob(src, dest_files):
    fs.movetree(src, "dest")
    assert set(Path().glob("dest/**/*.*")) == {Path(p) for p in dest_files}
    if src.startswith("root"):
        assert not list(Path().glob("src"))
    else:
        assert not list(Path().glob(f"root/{src}"))


@pytest.mark.usefixtures("tmp_dir")
@pytest.mark.parametrize(
    ("path", "root_files"),
    [
        (
            "**/*.txt",
            {"root/subdir-a/a-picture.png", "root/subdir-a/subdir-ac/ac-picture.png", "root/subdir-b/b-picture.png"},
        ),
        (
            "root/*a/*",
            {
                "root/subdir-a/subdir-ac/ac-file.txt",
                "root/subdir-a/subdir-ac/ac-picture.png",
                "root/subdir-b/b-file.txt",
                "root/subdir-b/b-picture.png",
            },
        ),
        (
            "root/*a/**/*.png",
            {
                "root/subdir-a/a-file.txt",
                "root/subdir-a/subdir-ac/ac-file.txt",
                "root/subdir-b/b-picture.png",
                "root/subdir-b/b-file.txt",
            },
        ),
    ],
)
def test_rmtree(path, root_files):
    fs.rmtree(path)
    assert set(Path().glob("root/**/*.*")) == {Path(p) for p in root_files}
    fs.rmtree(path)  # should not raise an exception
