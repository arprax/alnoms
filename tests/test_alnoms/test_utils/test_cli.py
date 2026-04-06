from unittest.mock import patch
from alnoms.cli import print_report, main


def test_print_report_no_empirical(capsys):
    """Ensures the CLI degrades gracefully if no data generator is found."""
    result = {
        "total_time": 1.0,
        "profile": [{"function": "test_func", "time": 0.5, "percent": 50}],
        "heuristics": [
            {
                "function": "test_func",
                "issue": "Bad loop",
                "complexity": "O(N)",
                "suggestion": "Fix",
            }
        ],
        "empirical": None,
        "empirical_target": None,
    }
    print_report(result, "test.py")
    captured = capsys.readouterr()
    assert "EMPIRICAL ANALYSIS SKIPPED" in captured.out
    assert "test_func()" in captured.out


def test_print_report_empirical_pass(capsys):
    """Ensures O(N) complexity passes the governance check."""
    result = {
        "total_time": 1.0,
        "profile": [],
        "heuristics": [],
        "empirical": [{"N": 10, "Time": 0.1, "Ratio": 0.0, "Complexity": "O(N)"}],
        "empirical_target": "fast_func",
    }
    print_report(result, "test.py")
    captured = capsys.readouterr()
    assert "PASSED: Function operates at O(N)" in captured.out


def test_print_report_empirical_fail(capsys):
    """Ensures O(N^2) complexity throws the governance failure."""
    result = {
        "total_time": 1.0,
        "profile": [],
        "heuristics": [],
        "empirical": [{"N": 10, "Time": 0.1, "Ratio": 0.0, "Complexity": "O(N^2)"}],
        "empirical_target": "slow_func",
    }
    print_report(result, "test.py")
    captured = capsys.readouterr()
    # assert "FAILED: Function operates at O(N^2)" in captured.out
    assert "Efficiency Warning" in captured.out
    assert "O(N^2)" in captured.out


@patch("alnoms.cli.analyze_file")
@patch("sys.argv", ["alnoms", "analyze", "dummy.py"])
def test_main_cli_execution(mock_analyze):
    """Ensures argparse routes the command correctly."""
    mock_analyze.return_value = {
        "total_time": 1.0,
        "profile": [],
        "heuristics": [],
        "empirical": None,
        "empirical_target": None,
    }
    main()
    mock_analyze.assert_called_once_with("dummy.py")
