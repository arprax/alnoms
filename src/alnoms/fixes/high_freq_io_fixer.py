"""
Alnoms Fixer: High‑Frequency I/O Remediation.

Provides the OSS remediation strategy for file or network I/O operations
executed inside loop bodies. High‑frequency I/O introduces significant
OS‑level overhead due to repeated system calls, context switching, and
kernel boundary transitions. This fixer offers:

    • Human‑readable explanation of the anti‑pattern
    • Before/after code snippets demonstrating buffered batching
    • Qualitative complexity shift estimates
    • OSS‑tier cure‑type classification (non‑auto‑patching)

Used by the HighFrequencyIODetector to surface actionable guidance when
loop‑bound I/O dominates runtime.
"""

from .base import Fixer


class HighFrequencyIOFixer(Fixer):
    """Remediation strategy for high‑frequency I/O operations inside loops.

    This fixer addresses patterns where file or network I/O is performed
    repeatedly within a loop body. Such operations incur significant
    OS‑level overhead due to system calls, context switching, and kernel
    boundary crossings. The recommended remediation is to buffer data in
    memory and perform a single batched write outside the loop.

    Attributes:
        pattern_id (str): Identifier for the associated detector pattern.
    """

    pattern_id = "high_freq_io"

    def explain(self, finding, detected_complexity="Unknown"):
        """Provides a human‑readable explanation of the optimization.

        Args:
            finding (Dict): The detector finding describing the I/O pattern.
            detected_complexity (str): The static or empirical complexity
                associated with the anti‑pattern.

        Returns:
            str: A narrative explanation describing why repeated I/O inside
            loops is slow and how batching mitigates the issue.
        """
        return (
            "I/O inside a tight loop is slow. "
            "Batch writes or accumulate data before writing."
        )

    def snippet_before_after(self, finding, detected_complexity="Unknown"):
        """Returns before/after code snippets illustrating the fix.

        Args:
            finding (Dict): The detector output for the high‑frequency I/O.
            detected_complexity (str): Complexity classification used to
                contextualize the snippet.

        Returns:
            Dict[str, str]: A dictionary containing:
                - ``before``: Example of repeated writes inside a loop.
                - ``after``: Example using a buffer and a single batched write.
        """
        before = "for row in rows:\n    file.write(format_row(row))"
        after = (
            "buffer = []\n"
            "for row in rows:\n"
            "    buffer.append(format_row(row))\n"
            "file.write(''.join(buffer))"
        )
        return {"before": before, "after": after}

    def cost_estimate(self, finding, detected_complexity="Unknown"):
        """Provides a qualitative estimate of the complexity improvement.

        Args:
            finding (Dict): The detector finding associated with the issue.
            detected_complexity (str): The complexity classification.

        Returns:
            Dict[str, str]: A dictionary describing expected improvements
            in time and memory complexity. Batching reduces repeated I/O
            calls and consolidates them into a single system interaction.
        """
        return {"time": "O(N * I/O) → O(I/O)", "memory": "O(N) buffer"}
