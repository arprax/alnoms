"""
Alnoms Fixer: Inefficient Membership Test Remediation.

Provides the OSS remediation strategy for inefficient membership checks
performed inside loop bodies. Patterns such as ``x in list`` or
``x in tuple`` incur O(N) lookup cost and can lead to accidental
quadratic or N*M behavior when nested. This fixer offers:

    • Human‑readable explanation of the anti‑pattern
    • Before/after code snippets demonstrating set‑based indexing
    • Qualitative complexity shift estimates
    • OSS‑tier cure‑type classification (non‑auto‑patching)

Used by the InefficientMembershipDetector to surface actionable guidance
when list‑based membership checks dominate runtime.
"""

from .base import Fixer


class InefficientMembershipFixer(Fixer):
    """Remediation strategy for inefficient membership tests inside loops.

    This fixer addresses patterns where membership checks such as
    ``x in list`` or ``x in tuple`` occur inside a loop. These operations
    are O(N) per lookup, leading to accidental O(N*M) or O(N²) behavior.
    The recommended remediation is to convert the container to a ``set``
    to achieve O(1) average‑case membership checks.

    Attributes:
        pattern_id (str): Identifier for the associated detector pattern.
    """

    pattern_id = "inefficient_membership"

    def explain(self, finding, detected_complexity="Unknown"):
        """Provides a human‑readable explanation of the optimization.

        Args:
            finding (Dict): The detector finding describing the membership pattern.
            detected_complexity (str): The static or empirical complexity
                associated with the anti‑pattern.

        Returns:
            str: A narrative explanation describing why list‑based membership
            checks inside loops are slow and how converting to a set improves
            performance.
        """
        return (
            "Membership checks on lists inside loops are O(N). "
            "Convert to a set for O(1) lookups."
        )

    def snippet_before_after(self, finding, detected_complexity="Unknown"):
        """Returns before/after code snippets illustrating the fix.

        Args:
            finding (Dict): The detector output for the inefficient membership test.
            detected_complexity (str): Complexity classification used to
                contextualize the snippet.

        Returns:
            Dict[str, str]: A dictionary containing:
                - ``before``: Example of repeated list membership checks.
                - ``after``: Example using a set for constant‑time lookups.
        """
        before = "for k in keys:\n    if k in items:\n        process(k)"
        after = (
            "items_set = set(items)\n"
            "for k in keys:\n"
            "    if k in items_set:\n"
            "        process(k)"
        )
        return {"before": before, "after": after}

    def cost_estimate(self, finding, detected_complexity="Unknown"):
        """Provides a qualitative estimate of the complexity improvement.

        Args:
            finding (Dict): The detector finding associated with the issue.
            detected_complexity (str): The complexity classification.

        Returns:
            Dict[str, str]: A dictionary describing expected improvements
            in time and memory complexity. Converting to a set reduces
            repeated O(N) scans to O(1) lookups.
        """
        return {"time": "O(N*M) → O(N + M)", "memory": "O(M)"}
