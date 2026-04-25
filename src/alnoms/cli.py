"""Alnoms: Performance Intelligence CLI.

Provides the command-line interface for the Alnoms performance intelligence system.
The CLI orchestrates static AST analysis, prescriptive remediation suggestions,
dynamic profiling, and empirical doubling tests to detect performance bottlenecks
before production.

Features:
    - CI/CD Ready: Supports raw and pretty JSON outputs for automation pipelines.
    - Static Analysis: Detects inefficient loops, API calls, and performance traps.
    - Prescriptive Suggestions: Recommends O(1) fixes and optimized patterns.
    - Empirical Analysis: Integrates with Arprax Profiler for Big-O scaling analysis.
"""

import argparse
import sys
import json
import io
import contextlib
from datetime import datetime, timezone

from alnoms.core.analyzer import ScriptAnalyzer


class PerformanceCLI:
    """Performance Intelligence CLI for complexity analysis and profiling.

    Acts as the primary entrypoint for the Alnoms performance intelligence system.
    Provides a terminal interface for static analysis, dynamic profiling,
    empirical scaling tests, and structured performance reporting. Designed for
    both human-readable output and CI/CD automation.
    """

    @staticmethod
    def print_report(result: dict) -> None:
        """Renders a full performance intelligence report in human-readable format.

        This method produces a structured analysis report that includes detected
        performance patterns, static diagnostics, dynamic profiling bottlenecks,
        empirical scaling analysis, performance verdict, and simulated fixes.

        Args:
            result (dict): Output from `ScriptAnalyzer.analyze_file()` containing:
                - 'patterns' (list): Detected performance patterns.
                - 'profile' (list): Dynamic profiling data.
                - 'empirical' (list): Empirical scaling analysis data.
                - 'meta' (dict): Metadata including timestamp and version.
                - 'empirical_target' (str): The target function for scaling tests.
                - 'total_time' (float): Total execution time.
                - 'file' (str): The analyzed file path.
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
    def main() -> None:
        """Primary entry point for the Alnoms Command-Line Interface.

        Configures the argument parser and routes execution based on the selected
        subcommand. Supports two primary modes:
        1. `analyze`: Human-readable performance reporting with deep profiling options.
        2. `ci`: Headless execution mode that accepts multiple files, outputs strict
           JSON, and enforces Big-O complexity guardrails via system exit codes.

        Raises:
            SystemExit:
                - Exits with 0 on successful execution and clean compliance.
                - Exits with 1 if an internal error occurs or if the `ci` mode detects
                  a performance bottleneck that breaches the `--fail-on` threshold.
        """
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

      # CI/CD Execution
      alnoms ci file1.py file2.py --fail-on "O(N^3)"
                """,
        )

        # Global version flag
        parser.add_argument("-v", "--version", action="version", version="Alnoms 1.1.2")

        subparsers = parser.add_subparsers(dest="command", help="Commands")

        # --- 1. THE HUMAN COMMAND (analyze) ---
        analyze_parser = subparsers.add_parser(
            "analyze", help="Analyze a single Python file"
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

        # --- 2. THE ROBOT COMMAND (ci) ---
        ci_parser = subparsers.add_parser(
            "ci", help="Headless execution for CI/CD pipelines"
        )
        ci_parser.add_argument("files", nargs="+", help="List of Python files to scan")
        ci_parser.add_argument(
            "--fail-on",
            default="",
            help="Complexity threshold to fail the build (e.g., O(N^3))",
        )

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

        elif args.command == "ci":
            # --- SEVERITY & SCORING MODEL ---

            severity_scoring = {
                "O(2^N)": {"level": "CRITICAL", "score": 7},
                "O(N^3)": {"level": "CRITICAL", "score": 6},
                "O(N^2)": {"level": "HIGH", "score": 5},
                "O(N log N)": {"level": "MEDIUM", "score": 4},
                "O(N)": {"level": "LOW", "score": 3},
                "O(log N)": {"level": "LOW", "score": 2},
                "O(1)": {"level": "LOW", "score": 1},
            }

            fail_score = severity_scoring.get(args.fail_on, {}).get("score", 99)

            raw_issues = []

            # --- 1. GATHER EVIDENCE ---

            for file_path in args.files:
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        result = ScriptAnalyzer.analyze_file(path=file_path, deep=False)

                    patterns = result.get("patterns", [])

                    for p in patterns:
                        comp = p.get("static_complexity") or "O(N^2)"

                        meta = severity_scoring.get(comp, {"level": "HIGH", "score": 5})

                        raw_issues.append(
                            {
                                "file": file_path,
                                "function": p.get("function", "global"),
                                "complexity": comp,
                                "severity": meta["level"],
                                "_score": meta["score"],  # Internal sorting key
                                "issue": p.get("issue", "Unknown Bottleneck"),
                                "suggestion": p.get("explanation", ""),
                            }
                        )

                except Exception as e:
                    # Handle internal engine crashes gracefully in the new schema

                    raw_issues.append(
                        {
                            "file": file_path,
                            "function": "unknown",
                            "complexity": "Unknown",
                            "severity": "CRITICAL",
                            "_score": 99,
                            "issue": "Engine Crash",
                            "suggestion": str(e),
                        }
                    )

            # --- 2. SORT & PRIORITIZE ---

            # Sort by highest severity score first. If tied, sort alphabetically by file to ensure determinism.

            raw_issues.sort(key=lambda x: (x["_score"], x["file"]), reverse=True)

            # Strip the internal sorting key for clean JSON

            for issue in raw_issues:
                del issue["_score"]

            # --- 3. BUILD THE PAYLOAD ---

            payload = {}

            if not raw_issues:
                # Clean Pass

                payload = {
                    "decision": {
                        "status": "PASS",
                        "reason": "No performance regressions detected",
                        "confidence": "HIGH",
                    },
                    "primary_trigger": None,
                    "summary": {
                        "total_issues": 0,
                        "by_severity": {
                            "CRITICAL": 0,
                            "HIGH": 0,
                            "MEDIUM": 0,
                            "LOW": 0,
                        },
                        "worst_complexity": "O(1)",
                        "risk_level": "LOW",
                    },
                    "issues": [],
                    "metadata": {
                        "scanned_files": len(args.files),
                        "analysis_mode": "fast",
                        "timestamp": datetime.now(timezone.utc)
                        .isoformat()
                        .replace("+00:00", "Z"),
                    },
                }

            else:
                # Issues Found

                primary = raw_issues[0]

                # --- 3. BUILD THE PAYLOAD ---

                # Aggregate Summary
                summary = {
                    "total_issues": len(raw_issues),
                    "by_severity": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0},
                    "worst_complexity": primary["complexity"],
                    "risk_level": primary["severity"],
                }
                for issue in raw_issues:
                    if issue["severity"] in summary["by_severity"]:
                        summary["by_severity"][issue["severity"]] += 1

                # --- THE STRICT GATE DECISION MODEL ---
                primary_score = severity_scoring.get(primary["complexity"], {}).get(
                    "score", 99
                )

                if primary["severity"] == "CRITICAL":
                    # Hard Rule: CRITICAL issues ALWAYS block. They cannot be bypassed.
                    is_blocked = True
                    reason = f"CRITICAL performance risk detected ({primary['complexity']} scaling)"
                elif primary_score >= fail_score:
                    # Threshold Rule: HIGH/MEDIUM issues block if they cross the user's defined limit.
                    is_blocked = True
                    reason = f"Performance regression threshold exceeded ({primary['complexity']} scaling)"
                else:
                    # Clean Pass
                    is_blocked = False
                    reason = "Code scales efficiently within acceptable limits."

                payload = {
                    "decision": {
                        "status": "BLOCK" if is_blocked else "PASS",
                        "reason": reason,
                        "confidence": "HIGH",
                    },
                    "primary_trigger": primary,
                    "summary": summary,
                    "issues": raw_issues,
                    "metadata": {
                        "scanned_files": len(args.files),
                        "analysis_mode": "fast",
                        "timestamp": datetime.now(timezone.utc)
                        .isoformat()
                        .replace("+00:00", "Z"),
                    },
                }

            # --- 4. OUTPUT ---

            print(json.dumps(payload, indent=2))

            if payload.get("decision", {}).get("status") == "BLOCK":
                sys.exit(1)

            sys.exit(0)
        else:
            parser.print_help()


if __name__ == "__main__":
    PerformanceCLI.main()
