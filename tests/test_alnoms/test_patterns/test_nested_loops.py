import ast
import textwrap
from alnoms.patterns.nested_loops import NestedLoopDetector


def test_nested_loops_detects_quadratic():
    src = textwrap.dedent("""
    def foo(arr):
        for i in range(len(arr)):
            for j in range(len(arr)):
                if arr[i] == arr[j]:
                    pass
    """)
    tree = ast.parse(src)
    det = NestedLoopDetector()
    findings = det.detect(tree)
    assert len(findings) == 1
    f = findings[0]
    assert f["pattern_id"] == "nested_loops"
    assert f["complexity"] == "O(N^2)"
    assert f["intent"] in {"membership", "sorting", "dfs", "generic"}
