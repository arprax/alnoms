"""
Alnoms Fixer: Expensive Call Remediation.

Provides the OSS remediation strategy for expensive or non‑trivial
function calls executed inside loop bodies. This fixer is part of the
Alnoms prescriptive optimization pipeline and offers:

    • Human‑readable explanation of the anti‑pattern
    • Before/after code snippets demonstrating caching or hoisting
    • Qualitative complexity shift estimates
    • OSS‑tier cure‑type classification (non‑auto‑patching)

This module is used by the ExpensiveCallDetector to surface actionable
guidance when repeated function calls dominate runtime.
"""

from .base import Fixer


class ExpensiveCallFixer(Fixer):
    """Remediation strategy for expensive function calls inside loops.

    This fixer addresses patterns where a costly or non‑trivial function
    is repeatedly invoked within a loop body. Such calls often dominate
    runtime and can be optimized by caching, memoization, or hoisting the
    computation outside the loop.

    Attributes:
        pattern_id (str): Identifier for the associated detector pattern.
    """

    pattern_id = "expensive_calls"

    def explain(self, finding, detected_complexity="Unknown"):
        """Provides a human‑readable explanation of the optimization.

        Args:
            finding (Dict): The detector finding describing the expensive call.
            detected_complexity (str): The static or empirical complexity
                associated with the anti‑pattern.

        Returns:
            str: A narrative explanation describing why repeated expensive
            calls inside loops are harmful and how caching or hoisting
            mitigates the issue.
        """
        return (
            "A costly function call is executed repeatedly. "
            "Cache/memoize the result or hoist it outside the loop."
        )

    def snippet_before_after(self, finding, detected_complexity="Unknown"):
        """Returns before/after code snippets illustrating the fix.

        Args:
            finding (Dict): The detector output for the expensive call.
            detected_complexity (str): Complexity classification used to
                contextualize the snippet.

        Returns:
            Dict[str, str]: A dictionary containing:
                - ``before``: Example of repeated expensive calls.
                - ``after``: Example using caching to avoid recomputation.
        """
        before = (
            "for item in items:\n    value = expensive_fn(item)\n    process(value)"
        )
        after = (
            "cache = {}\n"
            "for item in items:\n"
            "    if item not in cache:\n"
            "        cache[item] = expensive_fn(item)\n"
            "    process(cache[item])"
        )
        return {"before": before, "after": after}

    def cost_estimate(self, finding, detected_complexity="Unknown"):
        """Provides a qualitative estimate of the complexity improvement.

        Args:
            finding (Dict): The detector finding associated with the issue.
            detected_complexity (str): The complexity classification.

        Returns:
            Dict[str, str]: A dictionary describing expected improvements
            in time and memory complexity. For expensive calls, caching
            typically reduces repeated work and improves asymptotic cost.
        """
        return {"time": "O(N * C) → O(N + unique(C))", "memory": "O(unique(C))"}
