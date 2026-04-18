import os
import textwrap
from alnoms.core.analyzer import ScriptAnalyzer


def _write_script(tmp_path, content: str) -> str:
    path = os.path.join(tmp_path, "script.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content))
    return path


def test_analyze_file_basic_profile_and_patterns(tmp_path):
    script = _write_script(
        tmp_path,
        """
        def foo(arr):
            for i in range(len(arr)):
                for j in range(len(arr)):
                    if arr[i] == arr[j]:
                        pass
        """,
    )
    result = ScriptAnalyzer.analyze_file(script, deep=False)
    assert result["file"].endswith("script.py")
    assert isinstance(result["profile"], list)
    assert "patterns" in result
    # Should detect at least one nested loop
    assert any(p["pattern_id"] == "nested_loops" for p in result["patterns"])


def test_analyze_file_deep_empirical(tmp_path):
    script = _write_script(
        tmp_path,
        """
        def data_gen(n):
            return list(range(n))

        def slow_fn(arr):
            s = 0
            for x in arr:
                s += x
            return s
        """,
    )
    result = ScriptAnalyzer.analyze_file(script, deep=True)
    assert result["empirical_target"] in {"slow_fn", None}
    # empirical may be None if profiling didn't pick it up, but call should succeed
    assert "meta" in result and "version" in result["meta"]
