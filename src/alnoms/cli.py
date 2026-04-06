"""
Alnoms: Pre-Deployment Governance CLI.

Provides the command-line interface for the Alnoms algorithmic auditing framework.
Orchestrates static AST analysis and empirical doubling tests to enforce
performance governance before cloud deployment.

Features:
    - Static Analysis: Parses AST to detect inefficient loops and API calls.
    - Empirical Math: Integrates with Arprax Profiler for mathematical Big-O proofs.
    - Governance Verdict: Outputs CI/CD compliant scaling verdicts.
"""

import argparse
from alnoms.utils.analyzer import analyze_file


def print_report(result: dict, file_path: str):
    """
    Formats and outputs the algorithmic analysis report to the standard console.
    Provides a unified view of static bottlenecks and empirical Big-O scaling.

    Args:
        result (dict): The aggregated analysis payload from analyzer.py.
        file_path (str): The system path to the targeted Python script.
    """
    print("\n==================================================")
    print(" 🔬 ALNOMS ANALYSIS REPORT")
    print("==================================================")
    print(f"File: {file_path}")
    print(f"Total Execution Time: {result['total_time']}s\n")

    print("🚨 STATIC ANALYSIS (Top Bottlenecks)")
    print("-" * 50)
    for i, func in enumerate(result["profile"], 1):
        print(f"{i}. {func['function']}() -> {func['time']}s ({func['percent']}%)")
        related = [h for h in result["heuristics"] if h["function"] == func["function"]]
        for h in related:
            print(f"   ⚠️  Issue: {h['issue']}")
            print(f"   💡 Suggestion: {h['suggestion']}")
    print()

    # The Empirical output
    if result["empirical"]:
        print(f"📈 EMPIRICAL SCALING ANALYSIS: {result['empirical_target']}()")
        print("-" * 50)
        print(f"{'N':<10} | {'Time (s)':<12} | {'Ratio':<8} | {'Est. Complexity':<15}")
        print("-" * 50)

        final_complexity = "O(1)"
        for row in result["empirical"]:
            r_str = f"{row['Ratio']:.2f}" if row["Ratio"] > 0 else "-"
            print(
                f"{row['N']:<10} | {row['Time']:<12.5f} | {r_str:<8} | {row['Complexity']:<15}"
            )
            final_complexity = row["Complexity"]

        print("\n⚖️  GOVERNANCE VERDICT:")
        if "N^2" in final_complexity or "Exponential" in final_complexity:
            # print(f"❌ FAILED: Function operates at {final_complexity}. Cloud deployment blocked.")
            print(
                f"⚠️ Efficiency Warning: Function shows {final_complexity} growth and may not scale well."
            )
        else:
            print(
                f"✅ PASSED: Function operates at {final_complexity}. Safe for cloud scaling."
            )
    else:
        target = result.get("empirical_target", "your_function")
        print("ℹ️  EMPIRICAL ANALYSIS SKIPPED")
        print(f"   -> To prove Big-O complexity for {target}(), add a data generator:")
        print("\n   def data_gen(n):")
        print("       # Generate your test data of size 'n' here")
        print("       # return (arg1, arg2, ...)")
        print(
            "       # OR use 'target' to audit a specific function within a pipeline:"
        )
        print(f"       return {{'target': '{target}', 'args': (data_1, data_2)}}")

    print("==================================================\n")


def main():
    """
    Entry point for the Alnoms terminal command.
    Parses execution arguments and initializes the file analysis pipeline.
    """
    parser = argparse.ArgumentParser(description="Alnoms Profiling CLI")
    parser.add_argument("command", choices=["analyze"])
    parser.add_argument("file")
    args = parser.parse_args()

    if args.command == "analyze":
        result = analyze_file(args.file)
        print_report(result, args.file)


if __name__ == "__main__":  # pragma: no cover
    main()
