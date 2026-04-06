from alnoms.utils.heuristics import analyze_code


def test_clean_code(tmp_path):
    """Ensures O(1) built-ins do not trigger false positives."""
    code = """
def clean_func():
    arr = list(range(10))
    for i in arr:
        # Removed print(i) because it now correctly triggers 
        # the High-Frequency I/O detector.
        x = i + 1 
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


def test_redundant_sorting(tmp_path):
    """Ensures sorting inside loops is flagged as a scaling risk."""
    code = """
def slow_sort():
    data = [5, 2, 9]
    for i in range(100):
        data.sort()  # O(N^2 log N) risk
        sorted(data) # O(N^2 log N) risk
"""
    p = tmp_path / "sort.py"
    p.write_text(code)
    issues = analyze_code(str(p))
    # Should catch both the .sort() attribute and sorted() call
    assert any("Redundant sorting" in issue["issue"] for issue in issues)


def test_high_frequency_io(tmp_path):
    """Ensures I/O operations inside loops are identified."""
    code = """
def io_heavy():
    for i in range(10):
        with open("test.txt", "w") as f:
            f.write("data")
"""
    p = tmp_path / "io.py"
    p.write_text(code)
    issues = analyze_code(str(p))
    assert any("High-frequency I/O" in issue["issue"] for issue in issues)


def test_inplace_concatenation(tmp_path):
    """Ensures += operations inside loops are flagged."""
    code = """
def concat_func():
    s = ""
    for i in range(10):
        s += str(i) # O(N^2) memory risk
"""
    p = tmp_path / "concat.py"
    p.write_text(code)
    issues = analyze_code(str(p))
    assert any("In-place concatenation" in issue["issue"] for issue in issues)


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
    assert any(
        "Expensive call to 'external_api_call()'" in issue["issue"] for issue in issues
    )


def test_ast_parse_error(tmp_path):
    """Ensures the analyzer handles syntax errors gracefully."""
    code = "def broken_syntax(:"
    p = tmp_path / "broken.py"
    p.write_text(code)
    issues = analyze_code(str(p))
    assert len(issues) == 1
    assert "AST Analysis Error" in issues[0]["issue"]
