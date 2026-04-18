from alnoms.fixes.inefficient_membership_fixer import InefficientMembershipFixer


def test_inefficient_membership_fixer_explain():
    f = InefficientMembershipFixer()
    msg = f.explain({})
    assert "set" in msg.lower()


def test_inefficient_membership_fixer_snippets():
    f = InefficientMembershipFixer()
    s = f.snippet_before_after({})
    assert "set" in s["after"].lower()
