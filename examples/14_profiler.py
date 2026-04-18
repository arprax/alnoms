"""
Demo 14: Profiler Usage

Shows how to:
1. Benchmark a function
2. Run a doubling test
3. Use the @profile decorator
4. Run a stress suite for head‑to‑head comparisons
"""

from alnoms.core.profiler import Profiler


# ---------------------------------------------------------
# Example algorithms
# ---------------------------------------------------------


def linear_sum(arr):
    total = 0
    for x in arr:
        total += x
    return total


def quadratic_pairs(arr):
    count = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            count += arr[i] * arr[j]
    return count


def random_array(n):
    return [i for i in range(n)]


# ---------------------------------------------------------
# Demo
# ---------------------------------------------------------


def demo_profiler():
    print("\n=== Profiler Demo ===\n")

    profiler = Profiler(repeats=5, warmup=1, mode="min")

    # 1. Benchmark a single function
    print("1) Benchmarking linear_sum...")
    t = profiler.benchmark(linear_sum, random_array(10_000))
    print(f"   Time: {t:.6f}s\n")

    # 2. Doubling test
    print("2) Doubling Test on quadratic_pairs...")
    results = profiler.run_doubling_test(
        quadratic_pairs, random_array, start_n=200, rounds=4
    )
    profiler.print_analysis("quadratic_pairs", results)

    # 3. Decorator usage
    print("\n3) Decorator profiling...")

    @profiler.profile
    def decorated_sum(arr):
        return sum(arr)

    decorated_sum(random_array(50_000))
    decorated_sum(random_array(50_000))
    profiler.print_decorator_report()

    # 4. Stress suite
    print("\n4) Stress suite comparison...")
    suite = profiler.run_stress_suite(
        funcs={
            "linear_sum": linear_sum,
            "quadratic_pairs": quadratic_pairs,
        },
        input_gen=random_array,
        n_values=[500, 1000, 2000],
    )

    for n, row in suite.items():
        print(f"N = {n}: {row}")


if __name__ == "__main__":
    demo_profiler()
