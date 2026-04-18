"""
Alnoms Fixer: Redundant Sorting Remediation.

Provides the OSS remediation strategy for sorting operations executed
inside loop bodies. Repeated calls to ``sorted()`` or list ``.sort()``
within a loop introduce O(M log M) work per iteration, often resulting in
O(N * M log M) behavior. This fixer offers guidance on hoisting sorting
logic outside the loop or precomputing sorted structures.

This module provides:

    • Human‑readable explanation of the redundant‑sort anti‑pattern
    • Before/after code snippets demonstrating precomputation
    • Qualitative complexity shift estimates
    • OSS‑tier cure‑type classification (non‑auto‑patching)

Used by the RedundantSortDetector to surface actionable guidance when
loop‑bound sorting dominates runtime.
"""

from .base import Fixer


class RedundantSortFixer(Fixer):
    """Remediation strategy for redundant sorting operations inside loops.

    This fixer addresses patterns where `sorted()` or list `.sort()` is
    repeatedly invoked inside a loop. Sorting is O(M log M), and performing
    it N times inside a loop leads to O(N * M log M) behavior. The recommended
    remediation is to precompute sorted structures once outside the loop or
    restructure the algorithm to avoid repeated sorting.

    Attributes:
        pattern_id (str): Identifier for the associated detector pattern.
    """

    pattern_id = "redundant_sort"

    def explain(self, finding, detected_complexity="Unknown"):
        """Provides a human‑readable explanation of the optimization.

        Args:
            finding (Dict): The detector finding describing the sorting pattern.
            detected_complexity (str): The static or empirical complexity
                associated with the anti‑pattern.

        Returns:
            str: A narrative explanation describing why sorting inside loops
            is expensive and how hoisting or precomputation mitigates the issue.
        """
        return (
            "Sorting inside a loop is expensive. "
            "Hoist the sort outside the loop or precompute sorted structures."
        )

    def snippet_before_after(self, finding, detected_complexity="Unknown"):
        """Returns before/after code snippets illustrating the fix.

        Args:
            finding (Dict): The detector output for the redundant sorting pattern.
            detected_complexity (str): Complexity classification used to
                contextualize the snippet.

        Returns:
            Dict[str, str]: A dictionary containing:
                - ``before``: Example of repeated sorting inside a loop.
                - ``after``: Example using precomputation to avoid repeated sorting.
        """
        before = (
            "for chunk in chunks:\n"
            "    sorted_chunk = sorted(chunk)\n"
            "    process(sorted_chunk)"
        )
        after = (
            "# Precompute once\n"
            "sorted_chunks = [sorted(c) for c in chunks]\n"
            "for sc in sorted_chunks:\n"
            "    process(sc)"
        )
        return {"before": before, "after": after}

    def cost_estimate(self, finding, detected_complexity="Unknown"):
        """Provides a qualitative estimate of the complexity improvement.

        Args:
            finding (Dict): The detector finding associated with the issue.
            detected_complexity (str): The complexity classification.

        Returns:
            Dict[str, str]: A dictionary describing expected improvements
            in time and memory complexity. Precomputing sorted structures
            avoids repeated O(M log M) work inside the loop.
        """
        return {"time": "O(N * M log M) → O(N log M)", "memory": "O(N*M)"}
