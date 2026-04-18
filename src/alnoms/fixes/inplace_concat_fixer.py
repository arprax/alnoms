"""
Alnoms Fixer: In‑Place Concatenation Remediation.

Provides the OSS remediation strategy for inefficient string or list
concatenation performed inside loop bodies. Patterns such as ``result += s``
trigger repeated memory reallocations for strings and repeated list
copying for list concatenation, often resulting in O(N²) behavior.

This fixer offers:

    • Human‑readable explanation of the anti‑pattern
    • Before/after code snippets demonstrating list accumulation
    • Qualitative complexity shift estimates
    • OSS‑tier cure‑type classification (non‑auto‑patching)

Used by the InplaceConcatDetector to surface actionable guidance when
loop‑bound concatenation dominates runtime.
"""

from .base import Fixer


class InplaceConcatFixer(Fixer):
    """Remediation strategy for in‑place string or list concatenation inside loops.

    This fixer addresses patterns where `+=` or similar concatenation
    operations are used repeatedly inside a loop. Because Python strings
    are immutable and list concatenation reallocates memory, this pattern
    often results in O(N²) behavior. The recommended remediation is to
    accumulate items in a list and perform a single `join()` or `extend()`
    operation after the loop.

    Attributes:
        pattern_id (str): Identifier for the associated detector pattern.
    """

    pattern_id = "inplace_concat"

    def explain(self, finding, detected_complexity="Unknown"):
        """Provides a human‑readable explanation of the optimization.

        Args:
            finding (Dict): The detector finding describing the concatenation pattern.
            detected_complexity (str): The static or empirical complexity
                associated with the anti‑pattern.

        Returns:
            str: A narrative explanation describing why in‑place concatenation
            inside loops is costly and how list accumulation avoids repeated
            memory reallocations.
        """
        return (
            "String or list concatenation inside a loop is costly. "
            "Use list accumulation and join/extend instead."
        )

    def snippet_before_after(self, finding, detected_complexity="Unknown"):
        """Returns before/after code snippets illustrating the fix.

        Args:
            finding (Dict): The detector output for the in‑place concatenation.
            detected_complexity (str): Complexity classification used to
                contextualize the snippet.

        Returns:
            Dict[str, str]: A dictionary containing:
                - ``before``: Example of repeated concatenation inside a loop.
                - ``after``: Example using list accumulation and `join()`.
        """
        before = "result = ''\nfor s in strings:\n    result += s"
        after = (
            "parts = []\n"
            "for s in strings:\n"
            "    parts.append(s)\n"
            "result = ''.join(parts)"
        )
        return {"before": before, "after": after}

    def cost_estimate(self, finding, detected_complexity="Unknown"):
        """Provides a qualitative estimate of the complexity improvement.

        Args:
            finding (Dict): The detector finding associated with the issue.
            detected_complexity (str): The complexity classification.

        Returns:
            Dict[str, str]: A dictionary describing expected improvements
            in time and memory complexity. Converting concatenation to list
            accumulation typically reduces O(N²) behavior to O(N).
        """
        return {"time": "O(N^2) → O(N)", "memory": "O(N)"}
