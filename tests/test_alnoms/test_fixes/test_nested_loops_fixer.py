from alnoms.fixes.nested_loops_fixer import NestedLoopFixer


def test_nested_loops_fixer_explain_membership():
    f = NestedLoopFixer()
    msg = f.explain({"loop_depth": 2, "intent": "membership"})
    assert "membership" in msg.lower()


def test_nested_loops_fixer_explain_sorting():
    f = NestedLoopFixer()
    msg = f.explain({"loop_depth": 2, "intent": "sorting"})
    assert "sort" in msg.lower()


def test_nested_loops_fixer_explain_dfs():
    f = NestedLoopFixer()
    msg = f.explain({"loop_depth": 2, "intent": "dfs"})
    assert "graph" in msg.lower()


def test_nested_loops_fixer_explain_cubic():
    f = NestedLoopFixer()
    msg = f.explain({"loop_depth": 3})
    assert "cubic" in msg.lower() or "triple" in msg.lower()


def test_nested_loops_fixer_snippets_have_before_after():
    f = NestedLoopFixer()
    s = f.snippet_before_after({"loop_depth": 2, "intent": "generic"})
    assert "before" in s and "after" in s
