import ast
import textwrap
from alnoms.patterns.inplace_concat import InplaceConcatDetector


def test_inplace_concat_on_string_flagged():
    src = textwrap.dedent("""
    def foo(strings):
        result = ""
        for s in strings:
            result += s
    """)
    tree = ast.parse(src)
    det = InplaceConcatDetector()
    findings = det.detect(tree)
    assert len(findings) == 1
    assert findings[0]["pattern_id"] == "inplace_concat"
