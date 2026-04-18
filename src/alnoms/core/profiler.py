"""
Profiler: Performance Profiling Tools.

Provides precision timing utilities, statistical benchmarking, and empirical
complexity estimation (via doubling tests) for research‑grade algorithm
analysis. Designed to operate without external dependencies and suitable for
both OSS and PRO tiers of the Alnoms ecosystem.
"""

import time
import timeit
import gc
import copy
import sys
import statistics
import functools
from contextlib import contextmanager
from typing import Callable, List, Dict, Any, Generator


class Profiler:
    """Industrial‑grade performance analyzer for algorithm benchmarking.

    The Profiler supports:

    - Precision timing using `timeit.default_timer`
    - Warmup runs to stabilize CPU cache and branch predictors
    - Statistical aggregation (min, mean, median)
    - Doubling‑test complexity estimation
    - Decorator‑based profiling for normal program flow
    - Stress‑suite benchmarking for head‑to‑head comparisons

    Attributes:
        repeats (int): Number of timed runs per benchmark.
        warmup (int): Number of untimed warmup runs.
        mode (str): Statistical mode for final timing ('min', 'mean', 'median').
    """

    def __init__(self, repeats: int = 5, warmup: int = 1, mode: str = "min"):
        """Initialize the Profiler with benchmark settings.

        Args:
            repeats (int): Number of timed runs per benchmark.
            warmup (int): Number of warmup runs to prime CPU cache.
            mode (str): Statistical mode ('min', 'mean', 'median').

        Notes:
            - `repeats` is clamped to at least 1.
            - `warmup` is clamped to at least 0.
        """
        self.repeats = max(1, repeats)
        self.warmup = max(0, warmup)
        self.mode = mode
        self._profile_stats = {}

    @contextmanager
    def stopwatch(self, label: str = "Block") -> Generator[None, None, None]:
        """Context manager for precision timing of a code block.

        Args:
            label (str): Identifier for the timed block.

        Yields:
            None: Execution of the wrapped block.

        Side Effects:
            - Records elapsed time under `self._profile_stats[label]`.
        """
        start = timeit.default_timer()
        try:
            yield
        finally:
            end = timeit.default_timer()
            elapsed = end - start
            self._profile_stats.setdefault(label, []).append(elapsed)

    def benchmark(self, func: Callable, *args: Any) -> float:
        """Benchmark a function with GC disabled for timing purity.

        Args:
            func (Callable): Function to benchmark.
            *args (Any): Arguments passed to the function.

        Returns:
            float: Execution time in seconds, aggregated using the configured mode.

        Notes:
            - Deepcopies arguments to avoid mutation across runs.
            - Disables garbage collection to reduce jitter.
        """
        # Warmup runs
        for _ in range(self.warmup):
            safe_args = copy.deepcopy(args)
            func(*safe_args)

        times = []
        gc_old = gc.isenabled()
        gc.disable()
        try:
            for _ in range(self.repeats):
                safe_args = copy.deepcopy(args)
                start = timeit.default_timer()
                func(*safe_args)
                end = timeit.default_timer()
                times.append(end - start)
        finally:
            if gc_old:
                gc.enable()

        # Statistical mode selection
        if self.mode == "median":
            return statistics.median(times)
        elif self.mode == "mean":
            return statistics.mean(times)
        return min(times)

    def run_doubling_test(
        self,
        func: Callable,
        input_gen: Callable[[int], Any],
        start_n: int = 50,
        rounds: int = 3,
        timeout: float = 15.0,
    ) -> List[Dict[str, Any]]:
        """Perform doubling analysis to estimate algorithmic complexity.

        Args:
            func (Callable): Algorithm under test.
            input_gen (Callable): Function generating input for size N.
            start_n (int): Initial input size.
            rounds (int): Number of doubling iterations.
            timeout (float): Maximum allowed runtime for the entire test.

        Returns:
            List[Dict[str, Any]]: A list of records containing:
                - "N": Input size
                - "Time": Execution time
                - "Ratio": T(2N) / T(N)
                - "Complexity": Estimated Big‑O class

        Notes:
            - Automatically increases recursion limit for deep algorithms.
            - Stops early if timeout is exceeded.
        """
        sys.setrecursionlimit(max(3000, sys.getrecursionlimit()))
        results = []
        prev_time = 0.0
        n = start_n
        start_clock = time.time()

        for _ in range(rounds):
            if time.time() - start_clock > timeout:
                break

            data = input_gen(n)
            args = data if isinstance(data, tuple) else (data,)
            curr_time = self.benchmark(func, *args)

            ratio = curr_time / prev_time if prev_time > 0 else 0.0
            complexity = self._guess_complexity(ratio)

            results.append(
                {"N": n, "Time": curr_time, "Ratio": ratio, "Complexity": complexity}
            )
            prev_time = curr_time
            n *= 2

        return results

    def profile(self, func: Callable) -> Callable:
        """Decorator for lightweight profiling during normal execution.

        Args:
            func (Callable): Function to wrap.

        Returns:
            Callable: Wrapped function that records execution time.

        Notes:
            - Stores timing data under `self._profile_stats[func.__name__]`.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = timeit.default_timer()
            result = func(*args, **kwargs)
            end = timeit.default_timer()
            elapsed = end - start
            self._profile_stats.setdefault(func.__name__, []).append(elapsed)
            return result

        return wrapper

    def print_decorator_report(self) -> None:
        """Print a summary table of all decorator‑tracked timings.

        Displays:
            - Function/block label
            - Number of calls
            - Average time
            - Total time
        """
        print("\n📝 ALNOMS PROFILE REPORT")
        print(
            f"{'Label/Function':<20} | {'Calls':<6} | {'Avg Time (s)':<12} | {'Total Time'}"
        )
        print("-" * 65)
        for fname, times in self._profile_stats.items():
            avg_t = statistics.mean(times) if times else 0.0
            total_t = sum(times)
            print(f"{fname:<20} | {len(times):<6} | {avg_t:<12.5f} | {total_t:.5f}")

    def _guess_complexity(self, ratio: float) -> str:
        """Map doubling ratios to approximate Big‑O complexity classes.

        Args:
            ratio (float): Ratio T(2N) / T(N).

        Returns:
            str: Estimated complexity class.

        Notes:
            - Thresholds are widened to account for CPU jitter and frequency scaling.
        """
        if ratio <= 0:
            return "Initial Round"
        if ratio < 1.4:
            return "O(1) / O(log N)"
        if ratio < 2.8:
            return "O(N)"
        if ratio < 5.5:
            return "O(N^2)"
        if ratio < 10.0:
            return "O(N^3)"
        return "High Growth / Exponential"

    def print_analysis(self, func_name: str, results: List[Dict[str, Any]]) -> None:
        """Print a formatted table from a doubling test.

        Args:
            func_name (str): Name of the analyzed function.
            results (List[Dict[str, Any]]): Output from `run_doubling_test`.
        """
        print(f"\n🔬 ANALYSIS: {func_name} (Mode: {self.mode})")
        print(f"{'N':<10} | {'Time (s)':<12} | {'Ratio':<8} | {'Est. Complexity':<15}")
        print("-" * 55)
        for row in results:
            r_str = f"{row['Ratio']:.2f}" if row["Ratio"] > 0 else "-"
            print(
                f"{row['N']:<10} | {row['Time']:<12.5f} | {r_str:<8} | {row['Complexity']:<15}"
            )

    def run_stress_suite(
        self,
        funcs: Dict[str, Callable],
        input_gen: Callable[[int], Any],
        n_values: List[int] = [1000, 2000, 4000],
    ) -> Dict[int, Dict[str, float]]:
        """Run multiple algorithms across multiple input sizes.

        Useful for head‑to‑head comparisons in research, teaching, and
        performance governance.

        Args:
            funcs (Dict[str, Callable]): Mapping of function names to callables.
            input_gen (Callable): Data generator for size N.
            n_values (List[int]): Input sizes to test.

        Returns:
            Dict[int, Dict[str, float]]:
                Nested mapping of `{N: {FunctionName: Time}}`.
        """
        suite_results = {}
        for n in n_values:
            suite_results[n] = {}
            data = input_gen(n)
            args = data if isinstance(data, tuple) else (data,)

            for name, func in funcs.items():
                suite_results[n][name] = self.benchmark(func, *args)
        return suite_results
