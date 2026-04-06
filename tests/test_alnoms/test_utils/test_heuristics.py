from alnoms.utils.heuristics import analyze_code


def test_clean_code(tmp_path):
    """Ensures O(1) built-ins do not trigger false positives."""
    code = """
def clean_func():
    arr = list(range(10))
    for i in arr:
        print(i)
        len(arr)
"""
    p = tmp_path / "clean.py"
    p.write_text(code)
    issues = analyze_code(str(p))
    assert len(issues) == 0


def test_nested_loops(tmp_path):
    """Ensures O(N^2) loops are caught and flagged."""
    code = """
def bad_func():
    for i in range(10):
        for j in range(10):
            pass
"""
    p = tmp_path / "bad.py"
    p.write_text(code)
    issues = analyze_code(str(p))
    assert len(issues) == 1
    assert issues[0]["issue"] == "Nested loop detected"
    assert issues[0]["function"] == "bad_func"


def test_expensive_call_in_loop(tmp_path):
    """Ensures non-standard function calls inside loops are flagged."""
    code = """
def external_api_call():
    pass

def slow_func():
    for i in range(10):
        external_api_call()
"""
    p = tmp_path / "slow.py"
    p.write_text(code)
    issues = analyze_code(str(p))

    assert len(issues) == 1
    assert "Expensive call to 'external_api_call()'" in issues[0]["issue"]
