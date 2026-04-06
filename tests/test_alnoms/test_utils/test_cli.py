from unittest.mock import patch
import sys
from alnoms.cli import print_report, main


def test_print_report_teaching_logic(capsys):
    """
    Ensures the CLI acts as a 'Teacher' by suggesting the correct
    data_gen signature and target pinning pattern.
    """
    result = {
        "total_time": 1.0,
        "profile": [{"function": "process_transactions", "time": 0.5, "percent": 50}],
        "heuristics": [],
        "empirical": None,
        "empirical_target": "process_transactions",
    }
    print_report(result, "complex_pipeline.py")
    captured = capsys.readouterr()

    # Verify the educational guidance is present
    assert "EMPIRICAL ANALYSIS SKIPPED" in captured.out
    assert "To prove Big-O complexity for process_transactions()" in captured.out
    assert "def data_gen(n):" in captured.out
    assert "return {'target': 'process_transactions'" in captured.out


def test_print_report_empirical_pass(capsys):
    """Ensures O(N) complexity passes the governance check with a success verdict."""
    result = {
        "total_time": 1.0,
        "profile": [],
        "heuristics": [],
        "empirical": [{"N": 1000, "Time": 0.05, "Ratio": 2.0, "Complexity": "O(N)"}],
        "empirical_target": "fast_func",
    }
    print_report(result, "test.py")
    captured = capsys.readouterr()
    assert "PASSED: Function operates at O(N)" in captured.out
    assert "Safe for cloud scaling" in captured.out


def test_print_report_empirical_fail(capsys):
    """Ensures O(N^2) complexity triggers the industrial Efficiency Warning."""
    result = {
        "total_time": 1.0,
        "profile": [],
        "heuristics": [],
        "empirical": [{"N": 1000, "Time": 0.5, "Ratio": 4.0, "Complexity": "O(N^2)"}],
        "empirical_target": "slow_func",
    }
    print_report(result, "test.py")
    captured = capsys.readouterr()
    assert "Efficiency Warning" in captured.out
    assert "O(N^2)" in captured.out
    assert "may not scale well" in captured.out


@patch("alnoms.cli.analyze_file")
def test_main_cli_execution(mock_analyze):
    """Ensures argparse routes the command correctly from the system entry point."""
    # Mocking sys.argv for the test duration
    with patch.object(sys, "argv", ["alnoms", "analyze", "dummy.py"]):
        mock_analyze.return_value = {
            "total_time": 1.0,
            "profile": [],
            "heuristics": [],
            "empirical": None,
            "empirical_target": None,
        }
        main()
        mock_analyze.assert_called_once_with("dummy.py")
