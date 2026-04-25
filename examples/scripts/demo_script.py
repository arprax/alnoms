# ---------------------------------------------------------
# ALNOMS CI GUARDRAIL - SMOKE TEST SUITE
# ---------------------------------------------------------
# This file contains intentional performance regressions
# to verify the Alnoms GitHub Action blocks the PR and
# formats the Markdown report correctly.


def quadratic_trap(n):
    """A simple O(N^2) trap to test the Alnoms Guardrail."""
    data = list(range(n))
    count = 0
    for x in data:
        if x in data:  # O(N) membership check inside an O(N) loop
            count += 1
    return count


def performance_regression_test(data):
    """A nested loop that scales poorly with moderate workloads."""
    # This nested lookup should trigger the Blocked logic
    for item in data:
        if item in data:
            print(f"Processing: {item}")


def exponential_disaster_test(items):
    """An explicitly terrible O(N^3) loop to test severe warnings."""
    for i in items:
        for j in items:
            for k in items:
                if i == j == k:
                    pass
