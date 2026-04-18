from alnoms.fixes.inplace_concat_fixer import InplaceConcatFixer


def test_inplace_concat_fixer_explain():
    f = InplaceConcatFixer()
    msg = f.explain({})
    assert "concatenation" in msg.lower()


def test_inplace_concat_fixer_snippets():
    f = InplaceConcatFixer()
    s = f.snippet_before_after({})
    assert "join" in s["after"].lower()
