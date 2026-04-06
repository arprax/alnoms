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
    code = """
def alnoms_data_gen(n):
    return list(range(n))

def process_data(arr):
    res = []
    for i in arr:
        res.append(i)
    return res

if __name__ == '__main__':
    process_data(alnoms_data_gen(10))
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
    assert total_time > 0
    assert any(r["function"] == "process_data" for r in results)


@patch("alnoms.utils.analyzer.Profiler")
def test_run_empirical_test(MockProfiler, dummy_script):
    """Ensures the analyzer correctly hooks into the Arprax Profiler."""
    mod = run_script(dummy_script)

    # Fake the slow mathematical test
    instance = MockProfiler.return_value
    instance.run_doubling_test.return_value = [
        {"N": 100, "Time": 0.1, "Ratio": 0, "Complexity": "O(N)"}
    ]

    res = run_empirical_test(mod, "process_data")
    assert res is not None
    assert res[0]["Complexity"] == "O(N)"

    # Test fallback if the user forgets the data generator
    res_missing = run_empirical_test(mod, "missing_function")
    assert res_missing is None


@patch("alnoms.utils.analyzer.run_empirical_test")
def test_analyze_file(mock_empirical, dummy_script):
    """Ensures the master orchestration function returns the correct payload."""
    mock_empirical.return_value = [{"Complexity": "O(N)"}]
    result = analyze_file(dummy_script)

    assert "profile" in result
    assert "heuristics" in result
    assert result["empirical_target"] == "process_data"
