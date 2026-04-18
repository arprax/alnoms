import ast
import textwrap
from alnoms.patterns.high_freq_io import HighFrequencyIODetector


def test_high_freq_io_detects_open_write():
    src = textwrap.dedent("""
    def foo(rows, path):
        for r in rows:
            with open(path, "a") as f:
                f.write(str(r))
    """)
    tree = ast.parse(src)
    det = HighFrequencyIODetector()
    findings = det.detect(tree)
    assert any("high-frequency" in f["issue"].lower() for f in findings)
