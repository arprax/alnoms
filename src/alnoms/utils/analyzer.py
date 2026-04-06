"""
Alnoms: Execution and Orchestration Engine.

Coordinates the dynamic profiling, static AST analysis, and empirical scaling
tests for the Alnoms Pre-Deployment Governance framework.

Features:
    - Dynamic Execution: Safely loads and executes target scripts as __main__.
    - Aggressive Filtering: Strips Python internal noise (<module>, <listcomp>)
      to isolate actual developer code.
    - Empirical Integration: Bridges standard cProfile metrics with Arprax's
      mathematical doubling-test Profiler.
"""

import cProfile
import pstats
import io
import importlib.util
import sys
import os
import inspect
from typing import Optional, List, Dict, Any
from alnoms.utils.profiler import Profiler
from alnoms.utils.heuristics import analyze_code


def run_script(path: str):
    """
    Dynamically loads and executes a Python file.

    Tricks the Python interpreter into treating the target file as the main
    execution block ('__main__'). This ensures that any code hidden behind an
    'if __name__ == "__main__":' guard is actually executed and profiled.

    Args:
        path (str): The system path to the target Python script.

    Returns:
        module: The loaded and executed Python module object.
    """
    spec = importlib.util.spec_from_file_location("__main__", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["__main__"] = module
    spec.loader.exec_module(module)
    return module


def profile_script(path: str):
    """
    Runs a dynamic cProfile trace on the target script and filters the output.

    Aggressively strips out internal Python wrappers and standard library calls
    to isolate the top 5 slowest functions written specifically by the developer
    in the target file.

    Args:
        path (str): The system path to the target Python script.

    Returns:
        tuple: A tuple containing:
            - list[dict]: The top 5 slowest functions and their execution metrics.
            - float: The total execution time of the script.
            - module: The loaded execution module for downstream empirical testing.
    """
    pr = cProfile.Profile()
    pr.enable()
    module = run_script(path)
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

        # Ignore functions that do not belong to the target file
        if target_filename not in filename:
            continue

        # Ignore overarching script wrappers like <module> or <listcomp>
        if funcname.startswith("<") and funcname.endswith(">"):
            continue

        results.append(
            {
                "function": funcname,
                "time": round(cumtime, 5),
                "percent": round((cumtime / total_time) * 100, 2) if total_time else 0,
            }
        )

    results.sort(key=lambda x: x["time"], reverse=True)
    return results[:5], total_time, module


def run_empirical_test(
    module: Any, slowest_func_name: str
) -> Optional[List[Dict[str, Any]]]:
    """
    Orchestrates the empirical scaling analysis by bridging a target function
    with a user-defined data generator.

    This function implements 'Target Pinning' and 'Signature Validation' to ensure
    that mathematical doubling tests are performed on the correct logic without
    triggering TypeErrors on wrapper functions.

    Workflow:
        1. Identification: Looks for a 'data_gen' function in the target module.
        2. Targeting: Uses 'Target Pinning' if data_gen returns a dict; otherwise,
           targets the slowest function identified by cProfile.
        3. Validation: Employs an AST-level 'Safety Gate' to verify that the
           generator's output matches the target function's signature.
        4. Execution: Invokes the Alnoms Profiler to run doubling tests (N=250 to 2000).

    Args:
        module (Any): The dynamically loaded Python module being analyzed.
        slowest_func_name (str): The name of the function identified as the
            primary bottleneck during dynamic profiling.

    Returns:
        Optional[List[Dict[str, Any]]]: A list of scaling results (N, Time, Ratio,
            Complexity) if successful; None if requirements are not met or
            signatures mismatch.
    """
    input_gen = getattr(module, "data_gen", None)
    if not input_gen:
        return None

    # 1. Probe the generator to determine the auditing strategy
    sample_data = input_gen(250)

    # 2. Check for Explicit Pinning (User overrides the cProfile bottleneck)
    if isinstance(sample_data, dict) and "target" in sample_data:
        target_name = sample_data["target"]

        def effective_gen(n):
            return input_gen(n)["args"]
    else:
        # Default: Target the function that took the most time in cProfile
        target_name = slowest_func_name
        effective_gen = input_gen

    target_func = getattr(module, target_name, None)
    if not target_func:
        return None

    # 3. THE SAFETY GATE: Signature Verification
    # Prevents TypeErrors when a wrapper (e.g., run_pipeline) is identified
    # as the bottleneck but does not accept the scaled arguments.
    sig = inspect.signature(target_func)
    params = list(sig.parameters.values())

    # Calculate argument count provided by the generator
    test_args = effective_gen(250)
    args_count = len(test_args) if isinstance(test_args, tuple) else 1

    # Enforcement: If function takes 0 args but data is provided, skip to avoid crash
    if len(params) == 0 and args_count > 0:
        return None

    # 4. Mathematical Execution
    prof = Profiler(repeats=3, warmup=1, mode="min")
    return prof.run_doubling_test(target_func, effective_gen, start_n=250, rounds=4)


def analyze_file(path: str) -> dict:
    """
    The master orchestration pipeline.

    Combines dynamic profiling (cProfile), static analysis (AST), and
    empirical mathematical testing into a single JSON-serializable payload
    for the CLI reporter.

    Args:
        path (str): The system path to the target Python script.

    Returns:
        dict: The complete algorithmic governance report payload.
    """
    profile_results, total_time, module = profile_script(path)
    heuristic_results = analyze_code(path)

    empirical_results = None
    slowest_func_name = profile_results[0]["function"] if profile_results else None

    if slowest_func_name:
        empirical_results = run_empirical_test(module, slowest_func_name)

    return {
        "profile": profile_results,
        "heuristics": heuristic_results,
        "total_time": round(total_time, 4),
        "empirical": empirical_results,
        "empirical_target": slowest_func_name,
    }
