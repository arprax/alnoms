import pytest
import sys
import json
from unittest.mock import patch
from alnoms.cli import PerformanceCLI


# --- FIXTURES ---


@pytest.fixture
def mock_analyzer_result():
    """Provides a comprehensive mock result to exercise all print_report branches."""
    return {
        "file": "slow_script.py",
        "total_time": 0.05,
        "meta": {"version": "1.0.0", "timestamp": "2026-04-15T23:00:00Z"},
        "patterns": [
            {
                "function": "slow_func",
                "line": 10,
                "issue": "Nested Loop",
                "explanation": "O(N^2) trap.",
                "dsa_meta": {
                    "complexity": "O(N)",
                    "module": "alnoms.dsa",
                    "tier": "OSS",
                },
                "cost_estimate": {"time": "O(N^2) -> O(N)"},
                "snippets": {"before": "for i in x:", "after": "s = set(x)"},
            }
        ],
        "profile": [{"function": "slow_func", "time": 0.04, "percent": 80.0}],
        "empirical_target": "slow_func",
        "empirical": [
            {"N": 100, "Time": 0.001, "Ratio": 0.0, "Complexity": "O(N^2)"},
            {"N": 200, "Time": 0.004, "Ratio": 4.0, "Complexity": "O(N^2)"},
        ],
    }


# --- TESTS ---


def test_print_report_with_full_data(mock_analyzer_result, capsys):
    """Exercises every visual branch of the human-readable report."""
    PerformanceCLI.print_report(mock_analyzer_result)
    captured = capsys.readouterr().out

    # Updated to match the new 'Performance Intelligence Engine' headers
    assert "⚖️ PERFORMANCE REPORT" in captured
    assert "slow_script.py" in captured
    assert "🚨 STATIC ANALYSIS" in captured
    assert "⏱️ DYNAMIC PROFILING" in captured
    assert "📈 EMPIRICAL SCALING ANALYSIS" in captured
    assert "⚖️ VERDICT" in captured

    # Updated to match the simulated optimization header
    assert "🔁 AFTER OPTIMIZATION (SIMULATED)" in captured


def test_print_report_empty_data(capsys):
    """Exercises the 'Safe/No Patterns' branches of the report."""
    empty_result = {"patterns": [], "profile": [], "empirical": None}
    PerformanceCLI.print_report(empty_result)
    captured = capsys.readouterr().out

    # Updated to match the specific strings in cli.py
    assert "✅ No performance issues detected" in captured
    assert "✅ No performance bottlenecks detected" in captured
    assert "ℹ️ EMPIRICAL ANALYSIS SKIPPED" in captured


@patch("alnoms.core.analyzer.ScriptAnalyzer.analyze_file")
def test_main_json_output(mock_analyze, tmp_path, capsys):
    """Verifies the --json flag correctly routes to json.dumps."""
    mock_analyze.return_value = {"status": "ok"}
    script = tmp_path / "test.py"
    script.write_text("pass")

    # Mock sys.argv to simulate: alnoms analyze test.py --json
    test_args = ["alnoms", "analyze", str(script), "--json"]
    with patch.object(sys, "argv", test_args):
        PerformanceCLI.main()

    captured = capsys.readouterr().out
    result = json.loads(captured)
    assert result["status"] == "ok"


@patch("alnoms.core.analyzer.ScriptAnalyzer.analyze_file")
def test_main_error_handling(mock_analyze, tmp_path, capsys):
    """Ensures the CLI exits with code 1 on analyzer failure."""
    mock_analyze.side_effect = Exception("File not found")
    script = tmp_path / "missing.py"

    test_args = ["alnoms", "analyze", str(script)]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as e:
            PerformanceCLI.main()
        assert e.value.code == 1

    captured = capsys.readouterr().out
    assert "❌ Error" in captured


def test_cli_help_no_args(capsys):
    """Verifies help is printed if no command is provided."""
    with patch.object(sys, "argv", ["alnoms"]):
        PerformanceCLI.main()

    captured = capsys.readouterr().out
    assert "Usage" in captured or "alnoms" in captured
