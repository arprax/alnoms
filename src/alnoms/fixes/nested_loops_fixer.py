"""
Alnoms Fixer: Nested Loop Remediation.

Provides the OSS remediation strategy for nested loop patterns, including
quadratic (O(N²)) and cubic (O(N³)) behaviors. This fixer performs
intent‑aware analysis to distinguish between membership scans, manual
sorting routines, DFS‑style adjacency traversal, and matrix‑multiplication‑
like triple loops.

This module offers:

    • Human‑readable explanations of nested‑loop anti‑patterns
    • Before/after code snippets tailored to detected intent
    • Qualitative complexity shift estimates
    • OSS‑tier cure‑type classification (non‑auto‑patching)
    • Heuristics for identifying matrix multiplication patterns

Used by the NestedLoopDetector to surface actionable guidance when
loop‑nesting depth or intent indicates algorithmic inefficiency.
"""

from .base import Fixer


class NestedLoopFixer(Fixer):
    """Remediation strategy for nested loop patterns.

    This fixer provides intent‑aware remediation for nested loops,
    distinguishing between cubic patterns (e.g., matrix multiplication)
    and quadratic patterns such as membership scans, manual sorting, and
    DFS‑like adjacency traversal. Recommendations include algorithmic
    redesign, vectorization, hashing, and use of efficient data
    structures.

    Attributes:
        pattern_id (str): Identifier for the associated detector pattern.
    """

    pattern_id = "nested_loops"

    # -----------------------------
    # Heuristics
    # -----------------------------

    def _looks_like_matrix_multiply(self, finding):
        """Detects matrix‑multiplication‑like triple‑nested loops.

        This heuristic checks for patterns resembling:

            A[i][k] * B[k][j]

        It is intentionally conservative to avoid false positives.

        Args:
            finding (Dict): The detector finding containing source context.

        Returns:
            bool: True if the code resembles matrix multiplication.
        """
        code = finding.get("source", "") or ""
        code_lower = code.lower()

        return (
            "*" in code
            and "[" in code
            and "]" in code
            and ("a[" in code_lower or "matrix" in code_lower)
            and ("b[" in code_lower or "matrix" in code_lower)
        )

    # -----------------------------
    # Explanation
    # -----------------------------

    def explain(self, finding, detected_complexity="Unknown"):
        """Provides a human‑readable explanation of the nested loop issue.

        This method generates intent‑aware explanations for nested loops,
        distinguishing between cubic and quadratic patterns. It also
        provides domain‑specific guidance for matrix multiplication,
        membership scans, sorting‑like routines, and DFS‑style traversal.

        Args:
            finding (Dict): The detector finding describing the nested loop.
            detected_complexity (str): Static or empirical complexity.

        Returns:
            str: A narrative explanation describing the issue and the
            recommended remediation strategy.
        """
        depth = finding.get("loop_depth", 1)
        intent = finding.get("intent", "generic")

        # --- Cubic Cases ---
        if depth >= 3:
            if self._looks_like_matrix_multiply(finding):
                return (
                    "Cubic complexity detected (Matrix Multiplication Pattern). "
                    "This is a classic O(N^3) algorithm. High risk for production. "
                    "Use vectorized linear algebra (NumPy / BLAS) for 10x–100x speedups."
                )
            return (
                "Cubic complexity detected. This triple-nested loop is a high-risk "
                "algorithmic bottleneck. Consider pruning, memoization, or reducing "
                "the search space."
            )

        # --- Quadratic Cases (Intent-Aware) ---
        if intent == "membership":
            return (
                "This nested loop appears to perform membership or pairwise comparison. "
                "Use a hash-based index (set or dict) to reduce O(N^2) lookups to O(N)."
            )

        if intent == "sorting":
            return (
                "This nested loop resembles a manual sorting routine (e.g., bubble sort). "
                "Replace with an O(N log N) sorting algorithm such as merge sort."
            )

        if intent == "dfs":
            return (
                "This nested loop resembles a graph traversal pattern. "
                "Use a visited set and adjacency list to avoid redundant scanning."
            )

        return (
            "This nested loop likely causes O(N^2) behavior. "
            "Consider algorithmic redesign, pruning, or using more efficient data structures."
        )

    # -----------------------------
    # Snippets
    # -----------------------------

    def snippet_before_after(self, finding, detected_complexity="Unknown"):
        """Returns before/after code snippets illustrating the fix.

        Snippets are intent‑aware and tailored to the specific nested loop
        pattern detected. Cubic patterns receive vectorization or pruning
        guidance, while quadratic patterns receive hashing, sorting, or
        DFS‑related improvements.

        Args:
            finding (Dict): The detector finding describing the nested loop.
            detected_complexity (str): Complexity classification.

        Returns:
            Dict[str, str]: A dictionary containing:
                - ``before``: Example of the inefficient nested loop.
                - ``after``: Example of the recommended remediation.
        """
        depth = finding.get("loop_depth", 1)
        intent = finding.get("intent", "generic")

        # --- Cubic + Matrix Multiplication ---
        if depth >= 3 and self._looks_like_matrix_multiply(finding):
            before = (
                "# Triple-nested loop matrix multiplication\n"
                "for i in range(N):\n"
                "    for j in range(N):\n"
                "        for k in range(N):\n"
                "            C[i][j] += A[i][k] * B[k][j]"
            )
            after = (
                "# Use Vectorized Library (NumPy) or BLAS\n"
                "import numpy as np\n"
                "C = np.matmul(A, B)"
            )
            return {"before": before, "after": after}

        # --- Generic Cubic Fallback ---
        if depth >= 3:
            before = (
                "# Triple-nested loop\n"
                "for i in range(N):\n"
                "    for j in range(N):\n"
                "        for k in range(N):\n"
                "            work(i, j, k)"
            )
            after = (
                "# Consider pruning, memoization, or reducing search space\n"
                "optimized = optimized_algorithm(data)"
            )
            return {"before": before, "after": after}

        # --- Quadratic Membership Fix ---
        if intent == "membership":
            before = (
                "for a in A:\n"
                "    for b in B:\n"
                "        if a == b:\n"
                "            process(a)"
            )
            after = (
                "index = set(B)\nfor a in A:\n    if a in index:\n        process(a)"
            )
            return {"before": before, "after": after}

        # --- Sorting-Like Fix ---
        if intent == "sorting":
            before = (
                "# Manual quadratic sorting (e.g., bubble sort)\n"
                "for i in range(len(arr)):\n"
                "    for j in range(len(arr) - 1):\n"
                "        if arr[j] > arr[j + 1]:\n"
                "            arr[j], arr[j + 1] = arr[j + 1], arr[j]"
            )
            after = "# Replace with O(N log N) sort\narr = sorted(arr)"
            return {"before": before, "after": after}

        # --- DFS-Like Fix ---
        if intent == "dfs":
            before = (
                "# DFS-like nested loop\n"
                "for node in graph:\n"
                "    for neighbor in graph[node]:\n"
                "        process(node, neighbor)"
            )
            after = (
                "# Use visited set to avoid redundant scanning\n"
                "visited = set()\n"
                "def dfs(node):\n"
                "    if node in visited:\n"
                "        return\n"
                "    visited.add(node)\n"
                "    for neighbor in graph[node]:\n"
                "        dfs(neighbor)"
            )
            return {"before": before, "after": after}

        # --- Generic Quadratic Fallback ---
        before = (
            "# Quadratic nested loop\n"
            "for i in range(N):\n"
            "    for j in range(N):\n"
            "        work(i, j)"
        )
        after = (
            "# Consider algorithmic redesign or pruning\n"
            "optimized = optimized_algorithm(data)"
        )
        return {"before": before, "after": after}

    # -----------------------------
    # Cost Estimate
    # -----------------------------

    def cost_estimate(self, finding, detected_complexity="Unknown"):
        """Provides a qualitative estimate of the complexity improvement.

        Args:
            finding (Dict): The detector finding associated with the issue.
            detected_complexity (str): The complexity classification.

        Returns:
            Dict[str, str]: A dictionary describing expected improvements
            in time and memory complexity for cubic and quadratic cases.
        """
        depth = finding.get("loop_depth", 1)

        if depth >= 3:
            return {
                "time": "O(N^3) → O(N^2.8) or Hardware Vectorized",
                "memory": "Implementation Dependent",
            }

        return {
            "time": "O(N^2) → O(N)",
            "memory": "O(N) extra for set (if membership pattern)",
        }
