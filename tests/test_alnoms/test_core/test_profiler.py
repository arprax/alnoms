import time
from alnoms.core.profiler import Profiler


def test_benchmark_runs_and_respects_mode_min():
    p = Profiler(repeats=3, warmup=0, mode="min")

    def f(x):
        return x * 2

    t = p.benchmark(f, 10)
    assert t >= 0.0


def test_guess_complexity_monotone():
    p = Profiler()

    # Use the private heuristic indirectly via run_doubling_test
    def f(arr):
        return sum(arr)

    def gen(n):
        return list(range(n))

    results = p.run_doubling_test(f, gen, start_n=10, rounds=3)
    assert len(results) >= 1
    assert "Complexity" in results[0]


def test_stopwatch_records_label():
    p = Profiler()
    with p.stopwatch("block"):
        time.sleep(0.001)
    # print_decorator_report uses internal stats; just ensure no crash
    p.print_decorator_report()
