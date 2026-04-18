"""
Alnoms: Execution and Orchestration Engine.

Coordinates dynamic profiling, static AST analysis, empirical scaling tests,
and prescriptive remediation for the Alnoms Pre‑Deployment Governance
framework. This module serves as the central orchestrator that unifies:

    • Script execution in an isolated namespace
    • cProfile‑based dynamic performance profiling
    • Static AST pattern detection and loop‑depth analysis
    • Optional empirical doubling tests for complexity estimation
    • Metadata‑driven algorithm selection via the DecisionEngine
    • Fixer‑based prescriptive remediation and code‑level guidance
    • Unified governance report generation for downstream tooling

The engine is deterministic, side‑effect‑free, and designed for OSS‑tier
transparency. All orchestration logic is encapsulated in the ScriptAnalyzer
class, which exposes a single high‑level entrypoint: `analyze_file()`.
"""

import cProfile
import pstats
import io
import importlib.util
import sys
import os
import inspect
import ast
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from alnoms.core.profiler import Profiler
from alnoms.core.decision_engine import DecisionEngine
from alnoms.dsa.metadata import MetadataRegistry
from alnoms.patterns import analyze_code
from alnoms.fixes import get_fixer
from alnoms.core.generators import DataGenerator as std_gen
from alnoms.core.io import DataReader as std_io


class ScriptAnalyzer:
    """Central orchestrator for the Alnoms governance pipeline.

    This class coordinates:

    - Script execution and dynamic profiling
    - Static AST pattern detection
    - Loop‑depth and static complexity estimation
    - Optional empirical scaling tests
    - Metadata‑driven algorithmic recommendations
    - Fixer‑based prescriptive remediation

    All methods are static and the class is stateless.
    """

    # ----------------------------------------------------------------------
    # LOOP DEPTH ANALYSIS
    # ----------------------------------------------------------------------
    @staticmethod
    def _get_loop_depth(node: ast.AST) -> int:
        """Recursively compute the maximum nesting depth of loops.

        Comprehensions (list, dict, set, generator) are ignored because they
        are optimized internally by CPython and do not represent explicit
        nested loops in the same semantic sense.

        Args:
            node (ast.AST): The AST node to inspect.

        Returns:
            int: Maximum loop nesting depth. Returns 0 if no loops are found.
        """
        if isinstance(
            node, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)
        ):
            return 0

        if not isinstance(node, (ast.For, ast.While)):
            return 0

        max_child = 0
        for child in getattr(node, "body", []):
            max_child = max(max_child, ScriptAnalyzer._get_loop_depth(child))

        return 1 + max_child

    @staticmethod
    def _find_target_loop_node(tree: ast.AST, lineno: int) -> Optional[ast.AST]:
        """Locate the loop node closest to a given line number.

        This is a Python‑version‑safe method that does not rely on `end_lineno`.
        It finds the deepest loop whose starting line is less than or equal to
        the pattern's line number.

        Args:
            tree (ast.AST): Parsed AST of the entire file.
            lineno (int): Line number associated with a detected pattern.

        Returns:
            Optional[ast.AST]: The best matching loop node, or None.
        """
        best_match = None
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)) and hasattr(node, "lineno"):
                if node.lineno <= lineno:
                    if best_match is None or node.lineno > best_match.lineno:
                        best_match = node
        return best_match

    # ----------------------------------------------------------------------
    # SCRIPT EXECUTION & PROFILING
    # ----------------------------------------------------------------------
    @staticmethod
    def run_script(path: str):
        """Execute a Python script in an isolated module namespace.

        Args:
            path (str): Path to the Python script.

        Returns:
            module: The executed module object.
        """
        spec = importlib.util.spec_from_file_location("__main__", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["__main__"] = module
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def profile_script(path: str):
        """Profile a script and extract the top slowest developer functions.

        Uses `cProfile` to gather cumulative execution time and filters out
        non‑user code.

        Args:
            path (str): Path to the Python script.

        Returns:
            tuple: A tuple containing:
                - list: Top 5 slowest functions with timing info.
                - float: Total cumulative execution time.
                - module: The executed module object.
        """
        pr = cProfile.Profile()
        pr.enable()
        module = ScriptAnalyzer.run_script(path)
        pr.disable()

        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
        stats = ps.stats

        results = []
        total_time = sum([v[3] for v in stats.values()])
        target_filename = os.path.basename(path)

        for func, stat in stats.items():
            filename, lineno, funcname = func
            cumtime = stat[3]

            if target_filename not in filename:
                continue
            if funcname.startswith("<") and funcname.endswith(">"):
                continue

            results.append(
                {
                    "function": funcname,
                    "time": round(cumtime, 5),
                    "percent": round((cumtime / total_time) * 100, 2)
                    if total_time
                    else 0,
                }
            )

        results.sort(key=lambda x: x["time"], reverse=True)
        return results[:5], total_time, module

    # ----------------------------------------------------------------------
    # EMPIRICAL SCALING TESTS
    # ----------------------------------------------------------------------
    @staticmethod
    def run_empirical_test(
        module: Any,
        slowest_func_name: str,
        gen_name: str = None,
        data_file: str = None,
        start_n: int = 50,
        rounds: int = 3,
    ) -> Optional[List[Dict[str, Any]]]:
        """Run empirical doubling tests on a target function.

        Input data can come from:

        - A script‑defined `data_gen()`
        - A standard generator in `alnoms.core.generators`
        - A data file loaded via `DataReader`

        Args:
            module (Any): The executed script module.
            slowest_func_name (str): Function selected for empirical testing.
            gen_name (str, optional): Name of a standard generator.
            data_file (str, optional): Path to a data file.
            start_n (int): Initial input size.
            rounds (int): Number of doubling rounds.

        Returns:
            Optional[List[Dict[str, Any]]]: Empirical results or None.
        """
        input_gen = None

        # File-based generator
        if data_file:
            try:
                file_data = std_io.read_all_ints(data_file)
            except ValueError:
                file_data = std_io.read_lines(data_file)

            def input_gen(n):
                return (file_data[:n],)

        # Standard generator
        elif gen_name:
            raw_gen = getattr(std_gen, gen_name, None)

            def input_gen(n):
                res = raw_gen(n)
                return res if isinstance(res, tuple) else (res,)

        # Script-defined generator
        else:
            input_gen = getattr(module, "data_gen", None)

        if not input_gen:
            return None

        # Detect config overrides
        sample_data = input_gen(start_n)
        config = sample_data if isinstance(sample_data, dict) else {}
        final_start_n = config.get("start_n", start_n)
        final_rounds = config.get("rounds", rounds)

        # Determine target function
        if isinstance(sample_data, dict) and "target" in sample_data:
            target_name = sample_data["target"]

            def effective_gen(n):
                return input_gen(n)["args"]
        else:
            target_name = slowest_func_name

            def effective_gen(n):
                data = input_gen(n)
                return data if isinstance(data, tuple) else (data,)

        target_func = getattr(module, target_name, None)
        if not target_func:
            return None

        # Validate argument count
        sig = inspect.signature(target_func)
        required_params = [
            p
            for p in sig.parameters.values()
            if p.default == p.empty and p.kind not in (p.VAR_POSITIONAL, p.VAR_KEYWORD)
        ]

        test_args = effective_gen(final_start_n)
        args_count = len(test_args) if isinstance(test_args, tuple) else 1

        if args_count < len(required_params):
            return None

        prof = Profiler(repeats=3, warmup=1, mode="min")
        return prof.run_doubling_test(
            target_func, effective_gen, start_n=final_start_n, rounds=final_rounds
        )

    # ----------------------------------------------------------------------
    # FULL PIPELINE ORCHESTRATION
    # ----------------------------------------------------------------------
    @staticmethod
    def analyze_file(
        path: str,
        deep: bool = False,
        target_override: str = None,
        gen_name: str = None,
        data_file: str = None,
        start_n: int = 50,
        rounds: int = 3,
    ) -> dict:
        """Perform full governance analysis on a Python script.

        Pipeline:
            1. Execute + profile the script
            2. Run static AST pattern detection
            3. Compute loop depth and static complexity
            4. Optionally run empirical scaling tests
            5. Integrate DecisionEngine metadata
            6. Integrate Fixers for prescriptive remediation
            7. Produce a unified governance report

        Args:
            path (str): Path to the Python script.
            deep (bool): Whether to run empirical scaling tests.
            target_override (str, optional): Explicit function name for empirical tests.
            gen_name (str, optional): Name of a standard generator.
            data_file (str, optional): Path to a data file.
            start_n (int): Initial input size for empirical tests.
            rounds (int): Number of doubling rounds.

        Returns:
            dict: A complete governance analysis report.
        """
        # 1. Profile and Execute
        profile_results, total_time, module = ScriptAnalyzer.profile_script(path)

        # 2. Static Analysis
        raw_patterns = analyze_code(path)
        with open(path, "r") as f:
            full_tree = ast.parse(f.read())

        empirical_results = None
        slowest_func_name = profile_results[0]["function"] if profile_results else None
        empirical_target = target_override or slowest_func_name

        if deep and empirical_target:
            empirical_results = ScriptAnalyzer.run_empirical_test(
                module, empirical_target, gen_name, data_file, start_n, rounds
            )

        # 3. Decision Engine
        engine = DecisionEngine(MetadataRegistry.get_all())
        aggregated_findings = {}

        detected_complexity = (
            empirical_results[-1].get("Complexity", "Unknown")
            if empirical_results
            else "Unknown"
        )

        # 4. Remediation Orchestration
        for finding in raw_patterns:
            func = finding.get("function", "global")
            pid = finding.get("pattern_id", "unknown")
            line_no = finding.get("line")

            key = (func, pid)

            # Aggregate occurrences
            if key not in aggregated_findings:
                aggregated_findings[key] = finding
                finding["occurrence_count"] = 1
                finding["occurrence_lines"] = [line_no]
            else:
                aggregated_findings[key]["occurrence_count"] += 1
                aggregated_findings[key]["occurrence_lines"].append(line_no)
                continue

            # Static loop depth
            static_depth = 1
            if pid == "nested_loops":
                target_node = ScriptAnalyzer._find_target_loop_node(full_tree, line_no)
                if target_node:
                    static_depth = ScriptAnalyzer._get_loop_depth(target_node)

            finding["loop_depth"] = static_depth

            # Static vs empirical complexity
            finding["static_complexity"] = (
                f"O(N^{static_depth})" if pid == "nested_loops" else None
            )
            finding["empirical_complexity"] = detected_complexity

            # Decision Engine metadata
            is_cubic = (
                pid == "nested_loops" and static_depth >= 3
            ) or detected_complexity == "O(N^3)"

            if not is_cubic:
                recommended_algo = engine.decide_algorithm(pid)
                if recommended_algo:
                    finding["dsa_meta"] = engine.decide_metadata(recommended_algo)
            else:
                finding["dsa_meta"] = None
                finding["is_domain_override"] = True

            # Fixer integration
            fixer = get_fixer(pid)
            if fixer:
                finding["cure_type"] = fixer.cure_type()
                finding["explanation"] = fixer.explain(finding, detected_complexity)
                finding["cost_estimate"] = fixer.cost_estimate(
                    finding, detected_complexity
                )
                finding["snippets"] = fixer.snippet_before_after(
                    finding, detected_complexity
                )

        return {
            "file": path,
            "profile": profile_results,
            "patterns": list(aggregated_findings.values()),
            "total_time": round(total_time, 4),
            "empirical": empirical_results,
            "empirical_target": empirical_target,
            "meta": {
                "version": "0.1.3",
                "timestamp": datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
            },
        }
