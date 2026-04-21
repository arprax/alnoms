"""
Demo 18: End-to-End Governance Demonstration

This demonstration performs a complete governance audit on a deliberately
inefficient Python script. It exercises the full Alnoms pipeline:

  • Static AST analysis
  • Pattern detection and remediation metadata
  • Dynamic profiling (cProfile)
  • Empirical scaling (doubling test)
  • Governance verdict and impact summary

All narrative, impact, and recommendations are rendered by Alnoms itself
via PerformanceCLI.print_report(result).
"""

import os
from alnoms.core.analyzer import ScriptAnalyzer
from alnoms.cli import PerformanceCLI


DEMO_SCRIPT = """\
\"\"\"Inefficient script used for the Alnoms demonstration.\"\"\"

def slow_membership_sum(arr):
    total = 0
    for x in arr:
        # Intentional O(N^2) membership trap
        if x in arr:
            total += x
    return total

# Required for empirical scaling
def data_gen(n):
    return (list(range(n)),)

if __name__ == "__main__":
    data = list(range(200))
    print(slow_membership_sum(data))
"""


def write_demo_script() -> str:
    """Writes the demonstration script to a guaranteed location."""
    base_dir = os.path.join(os.getcwd(), "scripts")
    os.makedirs(base_dir, exist_ok=True)

    path = os.path.join(base_dir, "slow_script.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(DEMO_SCRIPT)

    print(f"📄 Demo script created at: {path}")
    return path


def run_governance_demo():
    print("\n==================================================")
    print("  ALNOMS END-TO-END GOVERNANCE DEMONSTRATION")
    print("==================================================\n")

    script_path = write_demo_script()
    print(f"Analyzing script: {script_path}\n")

    # High-level semantic interpretation for this demo (optional)
    print("🧠 DETECTED INTENT:")
    print("   Membership check inside loop (potential quadratic pattern)\n")

    # Full pipeline: static + profiling + empirical scaling
    result = ScriptAnalyzer.analyze_file(
        path=script_path,
        deep=True,
        target_override="slow_membership_sum",
        gen_name="random_array",
        data_file=None,
        start_n=50,
        rounds=4,
    )

    # Single call: Alnoms owns the entire report, including:
    # - context
    # - impact
    # - confidence
    # - after-fix simulation (if you implement it there)
    PerformanceCLI.print_report(result)

    print("\n==================================================")
    print("  DEMONSTRATION COMPLETE")
    print("==================================================\n")


if __name__ == "__main__":
    run_governance_demo()
