import ast
import textwrap
from alnoms.patterns.inefficient_membership import MembershipDetector


def test_membership_on_list_literal_flagged():
    src = textwrap.dedent("""
    def foo(xs):
        for x in xs:
            if x in [1, 2, 3, 4]:
                pass
    """)
    tree = ast.parse(src)
    det = MembershipDetector()
    findings = det.detect(tree)
    assert len(findings) == 1
    assert findings[0]["pattern_id"] == "inefficient_membership"
