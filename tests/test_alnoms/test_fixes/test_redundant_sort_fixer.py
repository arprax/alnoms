from alnoms.fixes.redundant_sort_fixer import RedundantSortFixer


def test_redundant_sort_fixer_explain():
    f = RedundantSortFixer()
    msg = f.explain({})
    assert "sort" in msg.lower()


def test_redundant_sort_fixer_snippets():
    f = RedundantSortFixer()
    s = f.snippet_before_after({})
    assert "before" in s and "after" in s
    assert "sorted" in s["after"]
