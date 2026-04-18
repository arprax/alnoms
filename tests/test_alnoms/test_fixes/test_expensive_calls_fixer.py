from alnoms.fixes.expensive_calls_fixer import ExpensiveCallFixer


def test_expensive_calls_fixer_explain():
    f = ExpensiveCallFixer()
    msg = f.explain({})
    assert "cache" in msg.lower() or "memo" in msg.lower()


def test_expensive_calls_fixer_snippets():
    f = ExpensiveCallFixer()
    s = f.snippet_before_after({})
    assert "before" in s and "after" in s
    assert "cache" in s["after"]
