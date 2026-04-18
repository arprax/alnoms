"""
Base Fixer Interface for Alnoms.

Defines the public OSS fixer contract used across the Alnoms remediation
pipeline. Fixers provide human‑readable explanations, before/after code
snippets, qualitative complexity improvements, and cure‑type taxonomy
metadata. OSS fixers do not perform auto‑patching; Pro/Enterprise tiers
override patch generation and safety checks.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional


class Fixer(ABC):
    """Abstract base class for all Alnoms fixers.

    A fixer provides prescriptive remediation for a detected anti‑pattern.
    OSS fixers focus on explanation, education, and developer guidance,
    while Pro/Enterprise fixers may override patch generation to perform
    safe automated refactoring.

    Attributes:
        pattern_id (str): Identifier of the pattern this fixer addresses.
    """

    pattern_id: str

    @abstractmethod
    def explain(self, finding: Dict, detected_complexity: str = "Unknown") -> str:
        """Generates a human‑readable explanation of the fix.

        Args:
            finding (Dict): The finding dictionary produced by the detector.
            detected_complexity (str): The static or empirical complexity
                associated with the anti‑pattern.

        Returns:
            str: A narrative explanation describing the issue and the
            recommended remediation strategy.
        """

    @abstractmethod
    def snippet_before_after(
        self, finding: Dict, detected_complexity: str = "Unknown"
    ) -> Dict[str, str]:
        """Provides before/after code snippets illustrating the fix.

        Args:
            finding (Dict): The detector output associated with the issue.
            detected_complexity (str): Complexity classification used to
                contextualize the snippet.

        Returns:
            Dict[str, str]: A dictionary with keys:
                - ``"before"``: Code illustrating the problematic pattern.
                - ``"after"``: Code showing the recommended remediation.
        """

    def cost_estimate(
        self, finding: Dict, detected_complexity: str = "Unknown"
    ) -> Dict[str, str]:
        """Provides a qualitative estimate of complexity improvement.

        OSS fixers return coarse‑grained qualitative shifts (e.g.,
        ``"O(N^2) → O(N)"``). Pro fixers may override this to provide
        more detailed or data‑driven estimates.

        Args:
            finding (Dict): The associated detector finding.
            detected_complexity (str): The complexity classification.

        Returns:
            Dict[str, str]: A dictionary describing expected improvements
            in time and memory complexity.
        """
        return {"time": "unknown", "memory": "unknown"}

    # -----------------------------
    # NEW: Cure Type Taxonomy
    # -----------------------------
    def cure_type(self) -> str:
        """Returns the category of optimization recommended by this fixer.

        Cure types help unify messaging across fixers and provide
        governance‑grade classification of remediation strategies.
        Examples include:

            • Data Structure Optimization
            • Algorithm Replacement
            • Loop Flattening
            • Memoization / Caching
            • General Optimization (default)

        Returns:
            str: The cure‑type classification for this fixer.
        """
        return "General Optimization"

    def generate_patch(self, source: str, finding: Dict) -> Optional[str]:
        """Generates an auto‑patch for the issue (OSS: disabled).

        OSS fixers do not modify source code. Pro/Enterprise fixers may
        override this method to produce safe, deterministic patches.

        Args:
            source (str): The full source code of the analyzed file.
            finding (Dict): The associated detector finding.

        Returns:
            Optional[str]: A patched version of the source code, or ``None``
            for OSS fixers.
        """
        return None

    def is_safe_to_apply(self, finding: Dict) -> bool:
        """Indicates whether the fixer can be auto‑applied.

        OSS fixers always return ``False`` because they do not perform
        automated refactoring. Pro/Enterprise fixers override this to
        signal when a patch is safe to apply without human review.

        Args:
            finding (Dict): The associated detector finding.

        Returns:
            bool: ``False`` for OSS fixers.
        """
        return False
