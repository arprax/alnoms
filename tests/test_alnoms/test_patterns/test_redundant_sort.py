import ast
import textwrap
from alnoms.patterns.redundant_sort import RedundantSortDetector


def test_redundant_sort_inside_loop():
    src = textwrap.dedent("""
    def foo(chunks):
        for c in chunks:
            s = sorted(c)
            print(s)
    """)
    tree = ast.parse(src)
    det = RedundantSortDetector()
    findings = det.detect(tree)
    assert len(findings) == 1
    f = findings[0]
    assert f["pattern_id"] == "redundant_sort"
    assert "sorting" in f["issue"].lower()
