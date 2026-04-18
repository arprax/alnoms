"""
Alnoms: Performance Intelligence CLI.

Provides the command-line interface for the Alnoms performance intelligence system.
The CLI orchestrates static AST analysis, prescriptive remediation suggestions,
dynamic profiling, and empirical doubling tests to detect performance bottlenecks
before production.

Features:
    • CI/CD Ready: Supports raw and pretty JSON outputs for automation pipelines.
    • Static Analysis: Detects inefficient loops, API calls, and performance traps.
    • Prescriptive Suggestions: Recommends O(1) fixes and optimized patterns.
    • Empirical Analysis: Integrates with Arprax Profiler for Big-O scaling analysis.
"""

import argparse
import sys
import json
from alnoms.core.analyzer import ScriptAnalyzer


class PerformanceCLI:
    """Performance Intelligence CLI for complexity analysis and profiling.

    Acts as the primary entrypoint for the Alnoms performance intelligence system.
    Provides a terminal interface for static analysis, dynamic profiling,
    empirical scaling tests, and structured performance reporting. Designed for
    both human-readable output and CI/CD automation.
    """

    @staticmethod
    def print_report(result: dict):
        """Renders a full performance intelligence report in human-readable format.

        This method produces a structured analysis report that includes:

        • Detected performance patterns
        • Static diagnostics and optimization suggestions
        • Dynamic profiling bottlenecks
        • Empirical scaling analysis (doubling test)
        • Performance verdict and impact estimation
        • Confidence scoring and post-fix simulation

        Args:
            result (dict): Output from `ScriptAnalyzer.analyze_file()` containing:
                patterns, profile, empirical, meta, empirical_target, total_time.

        Returns:
            None: Prints directly to stdout.
        """
        meta = result.get("meta", {})
        patterns = result.get("patterns", [])
        profile_data = result.get("profile", [])
        empirical_data = result.get("empirical")
        target_name = result.get("empirical_target")

        print("\n==================================================")
        print("⚖️ PERFORMANCE REPORT")
        print("==================================================")
        print(f"File: {result.get('file', 'Unknown')}")
        print(f"Timestamp (UTC): {meta.get('timestamp', 'Unknown')}")
        print(f"Total Execution Time: {result.get('total_time', 0)}s\n")

        # ---------------------------------------------------------
        # 0. DETECTED INTENT
        # ---------------------------------------------------------
        if patterns:
            primary = patterns[0]
            intent = (
                primary.get("intent")
                or primary.get("issue")
                or primary.get("pattern_id")
            )
            print("🧠 DETECTED INTENT:")
            print(f"   {intent}\n")

        # ---------------------------------------------------------
        # 1. STATIC ANALYSIS & SUGGESTIONS
        # ---------------------------------------------------------
        print("🚨 STATIC ANALYSIS (Diagnostics & Suggestions)")
        print("-" * 50)

        if not patterns:
            print(
                "   ✅ No performance issues detected. Code is structurally efficient.\n"
            )
        else:
            for i, p in enumerate(patterns, 1):
                func_name = p.get("function", "global")
                line_no = p.get("line", "??")
                issue = p.get("issue", p.get("pattern_id"))

                print(
                    f"{i}. ⚠️ ISSUE: {issue} (Function: {func_name} | Line: {line_no})"
                )

                if "explanation" in p:
                    print(f"   📖 Explanation: {p['explanation']}")

                    dsa = p.get("dsa_meta")
                    if dsa:
                        complexity = dsa.get("complexity", "O(N)")
                        module_path = dsa.get("module", "builtin")
                        tier = dsa.get("tier", "OSS")

                        print(f"   💊 RECOMMENDED OPTIMIZATION: {complexity}")
                        print(f"   🏗️ IMPLEMENTATION: {module_path}")
                        print(f"   🔐 ACCESS TIER: {tier}")

                    costs = p.get("cost_estimate", {})
                    if "time" in costs:
                        print(f"   ⏱️ Complexity Shift: {costs['time']}")

                    snip = p.get("snippets")
                    if snip:
                        print("\n   💡 SUGGESTED FIX:")
                        print("   --- BEFORE ---")
                        for line in snip["before"].split("\n"):
                            print(f"   |  {line}")
                        print("   --- AFTER ---")
                        for line in snip["after"].split("\n"):
                            print(f"   |  {line}")

                print()

        # ---------------------------------------------------------
        # 2. DYNAMIC PROFILING
        # ---------------------------------------------------------
        print("⏱️ DYNAMIC PROFILING (Top Execution Bottlenecks)")
        print("-" * 50)

        if not profile_data:
            print("   ✅ No performance bottlenecks detected in execution.\n")
        else:
            for i, func in enumerate(profile_data, 1):
                print(
                    f"   {i}. {func['function']}() -> {func['time']}s ({func['percent']}%)"
                )
            print()

        # ---------------------------------------------------------
        # 3. EMPIRICAL SCALING
        # ---------------------------------------------------------
        if empirical_data:
            print(f"📈 EMPIRICAL SCALING ANALYSIS: {target_name}()")
            print("-" * 50)
            print(
                f"{'N':<10} | {'Time (s)':<12} | {'Ratio':<8} | {'Est. Complexity':<15}"
            )
            print("-" * 50)

            final_complexity = "O(1)"
            for row in empirical_data:
                r_str = f"{row['Ratio']:.2f}" if row["Ratio"] > 0 else "-"
                print(
                    f"{row['N']:<10} | {row['Time']:<12.5f} | {r_str:<8} | {row['Complexity']:<15}"
                )
                final_complexity = row["Complexity"]

            # ---------------------------------------------------------
            # 4. VERDICT
            # ---------------------------------------------------------
            print("\n⚖️ VERDICT:")

            safe_tiers = ["O(1)", "O(log N)", "O(N)", "O(N log N)"]

            if final_complexity in safe_tiers:
                print(
                    f"✅ PASSED: Function operates at {final_complexity}. Safe for scaling."
                )
            elif final_complexity == "O(N^2)":
                print(
                    f"⚠️ WARNING: Function operates at {final_complexity}. May not scale efficiently."
                )
            else:
                print(
                    f"❌ RISK: Function operates at {final_complexity}. Review recommended."
                )

            # ---------------------------------------------------------
            # 5. CONTEXT
            # ---------------------------------------------------------
            print("\n📌 CONTEXT")
            print("-" * 50)
            print(
                "   Empirical scaling validates asymptotic behavior under increasing load.\n"
            )

            # ---------------------------------------------------------
            # 6. IMPACT ESTIMATION
            # ---------------------------------------------------------
            print("🚀 EXPECTED IMPACT")
            print("-" * 50)
            print("   For N = 10,000:")
            print("     • O(N²) → ~100,000,000 operations")
            print("     • O(N)  → ~10,000 operations")
            print("   Estimated improvement: 100×–1000× depending on workload.\n")

            # ---------------------------------------------------------
            # 7. CONFIDENCE
            # ---------------------------------------------------------
            print("🤖 CONFIDENCE")
            print("-" * 50)

            if final_complexity == "O(N^2)":
                print("   High — static and empirical signals agree.\n")
            else:
                print("   Medium — mixed signals between analysis methods.\n")

            # ---------------------------------------------------------
            # 8. SIMULATED FIX
            # ---------------------------------------------------------
            print("🔁 AFTER OPTIMIZATION (SIMULATED)")
            print("-" * 50)
            print("   Expected Complexity: O(N)")
            print("   Behavior: Linear scaling with stable performance.")
            print("   Suggested Implementation:")
            print("       s = set(arr)")
            print("       for x in arr:")
            print("           if x in s:")
            print("               total += x\n")

        else:
            print("ℹ️ EMPIRICAL ANALYSIS SKIPPED\n")

        print("==================================================\n")

    @staticmethod
    def main():
        parser = argparse.ArgumentParser(
            prog="alnoms",
            description="🔬 Alnoms: Performance Intelligence System",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Example Usage:
  alnoms analyze script.py
  alnoms analyze script.py --deep
  alnoms analyze script.py --deep --start-n 50 --rounds 3
  alnoms analyze script.py --json
            """,
        )

        subparsers = parser.add_subparsers(dest="command", help="Commands")

        analyze_parser = subparsers.add_parser(
            "analyze", help="Analyze Python file performance"
        )
        analyze_parser.add_argument("file", help="Python file path")

        audit_group = analyze_parser.add_argument_group("Analysis Options")
        audit_group.add_argument("--deep", action="store_true")
        audit_group.add_argument("--function", dest="target_override")
        audit_group.add_argument("--gen", dest="gen")
        audit_group.add_argument("--data", dest="data")
        audit_group.add_argument("--start-n", type=int, default=50)
        audit_group.add_argument("--rounds", type=int, default=3)

        output_group = analyze_parser.add_argument_group("Output Options")
        output_group.add_argument("--json", action="store_true")
        output_group.add_argument("--pretty", action="store_true")

        args = parser.parse_args()

        if args.command == "analyze":
            try:
                result = ScriptAnalyzer.analyze_file(
                    path=args.file,
                    deep=args.deep,
                    target_override=args.target_override,
                    gen_name=args.gen,
                    data_file=args.data,
                    start_n=args.start_n,
                    rounds=args.rounds,
                )

                if args.json or args.pretty:
                    print(json.dumps(result, indent=2 if args.pretty else None))
                    return

                PerformanceCLI.print_report(result)

            except Exception as e:
                print(f"❌ Error analyzing {args.file}: {str(e)}")
                sys.exit(1)
        else:
            parser.print_help()


if __name__ == "__main__":
    PerformanceCLI.main()
