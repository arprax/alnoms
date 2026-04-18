import os
from alnoms.core.io import DataReader


def _write(tmpdir, content: str) -> str:
    path = os.path.join(tmpdir, "data.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def test_read_all_ints_roundtrip(tmp_path):
    path = _write(tmp_path, "1 2\n3\t4")
    vals = DataReader.read_all_ints(str(path))
    assert vals == [1, 2, 3, 4]


def test_read_all_strings_roundtrip(tmp_path):
    path = _write(tmp_path, "alpha beta\ngamma")
    vals = DataReader.read_all_strings(str(path))
    assert vals == ["alpha", "beta", "gamma"]


def test_read_lines_preserves_empty(tmp_path):
    path = _write(tmp_path, "a\n\nb\n")
    vals = DataReader.read_lines(str(path))
    assert vals == ["a", "", "b"]
