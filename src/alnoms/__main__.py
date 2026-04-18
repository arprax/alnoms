"""
Alnoms Command‑Line Entrypoint.

Provides the executable entry surface for the Alnoms governance framework.
Running `python -m alnoms` invokes the PerformanceCLI, which exposes:

    • Static AST analysis
    • Dynamic profiling
    • Empirical scaling tests (optional)
    • Pattern detection and remediation reporting
    • Full pre‑deployment governance workflows

This module contains no business logic; it simply delegates execution to
the PerformanceCLI to ensure a clean separation between orchestration,
presentation, and CLI concerns.
"""

from alnoms.cli import PerformanceCLI

if __name__ == "__main__":
    PerformanceCLI.main()
