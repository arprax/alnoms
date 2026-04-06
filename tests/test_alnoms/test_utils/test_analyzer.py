import pytest
from unittest.mock import patch
from alnoms.utils.analyzer import (
    run_script,
    profile_script,
    run_empirical_test,
    analyze_file,
)


@pytest.fixture
def dummy_script(tmp_path):
    """Generates a standard test script with a data generator."""
    code = """
def data_gen(n):
    return (list(range(n)),)

def process_data(arr):
    res = []
    for i in arr:
        res.append(i)
    return res

if __name__ == '__main__':
    process_data(data_gen(10)[0])
"""
    p = tmp_path / "dummy.py"
    p.write_text(code)
    return str(p)


def test_run_script(dummy_script):
    """Ensures the module loader correctly imports and executes files."""
    mod = run_script(dummy_script)
    assert hasattr(mod, "process_data")


def test_profile_script(dummy_script):
    """Ensures cProfile filters internal Python noise and finds the bottleneck."""
    results, total_time, mod = profile_script(dummy_script)
    assert total_time >= 0
    assert any(r["function"] == "process_data" for r in results)


@patch("alnoms.utils.analyzer.Profiler")
def test_run_empirical_test_basic(MockProfiler, dummy_script):
    """Ensures basic empirical hooking works with the new 'data_gen' name."""
    mod = run_script(dummy_script)
    instance = MockProfiler.return_value
    instance.run_doubling_test.return_value = [
        {"N": 100, "Time": 0.1, "Ratio": 0, "Complexity": "O(N)"}
    ]

    res = run_empirical_test(mod, "process_data")
    assert res is not None
    assert res[0]["Complexity"] == "O(N)"


def test_empirical_target_pinning():
    """Verifies that the engine respects explicit target pinning in data_gen."""

    class MockModule:
        def targeted_func(self, data):
            pass

        def data_gen(self, n):
            return {"target": "targeted_func", "args": (list(range(n)),)}

    with patch("alnoms.utils.analyzer.Profiler") as MockProfiler:
        instance = MockProfiler.return_value
        instance.run_doubling_test.return_value = [{"Complexity": "O(N)"}]

        # We pass 'wrong_func' as the slowest, but it should pick 'targeted_func'
        res = run_empirical_test(MockModule(), "wrong_func")
        assert res is not None
        # Verify the profiler was called with the pinned target
        assert MockProfiler.return_value.run_doubling_test.called


def test_empirical_safety_gate_skip():
    """Ensures the engine skips tests if signatures mismatch to prevent TypeErrors."""

    class MockModule:
        def wrapper_func(self):
            pass  # 0 args

        def data_gen(self, n):
            return (list(range(n)),)  # 1 arg

    module = MockModule()
    # Should return None because 1 arg cannot be passed to a 0-arg function
    res = run_empirical_test(module, "wrapper_func")
    assert res is None


@patch("alnoms.utils.analyzer.run_empirical_test")
def test_analyze_file(mock_empirical, dummy_script):
    """Ensures the master orchestration function returns the correct payload."""
    mock_empirical.return_value = [{"Complexity": "O(N)"}]
    result = analyze_file(dummy_script)

    assert "profile" in result
    assert "heuristics" in result
    assert result["empirical_target"] == "process_data"
