import ast
import textwrap
from alnoms.patterns.expensive_calls import ExpensiveCallDetector


def test_expensive_calls_skips_safe_and_flags_custom():
    src = textwrap.dedent("""
    def foo(xs):
        for x in xs:
            y = len(xs)
            z = custom(x)
            print(y, z)
    """)
    tree = ast.parse(src)
    det = ExpensiveCallDetector()
    findings = det.detect(tree)
    # len and print are safe; custom should be flagged
    assert any("custom" in f["issue"] for f in findings)
    assert all("len" not in f["issue"] for f in findings)
