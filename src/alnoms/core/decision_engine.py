"""
Alnoms OSS Decision Engine.

This module implements the deterministic, rule‑based algorithm selection
mechanism for the OSS tier of the Alnoms optimization pipeline. The
DecisionEngine maps detected performance patterns to recommended
algorithmic remedies using static, non‑adaptive rules.

The OSS tier guarantees:
    • No telemetry
    • No learning or heuristics
    • No dynamic context overrides
    • Fully deterministic, reproducible behavior

The DecisionEngine sits between the pattern detectors and the fixers,
providing stable, governance‑aligned recommendations suitable for
open‑source usage and reproducible analysis.
"""

from typing import Optional, Dict


class DecisionEngine:
    """Deterministic rule‑based mapping for OSS‑tier algorithm selection.

    The DecisionEngine provides a stable, non‑adaptive mapping from detected
    performance patterns to recommended data‑structure or algorithmic
    remedies. All identifiers returned by this engine use **snake_case**
    to satisfy OSS‑tier test and governance requirements.

    Metadata lookup is also performed using snake_case keys, matching the
    canonical identifiers stored in the MetadataRegistry.
    """

    def __init__(self, metadata: Dict[str, dict]):
        """Initialize the decision engine with metadata.

        Args:
            metadata (Dict[str, dict]):
                Mapping of snake_case algorithm identifiers to metadata
                dictionaries. Each metadata entry typically includes
                complexity, category, tier, and module import path.
        """
        self.metadata = metadata

        # Base rules for non‑nested‑loop patterns (snake_case outward)
        self.rule_map = {
            "inefficient_membership": "separate_chaining_hash_st",
            "redundant_sort": "merge_sort",
            "inplace_concat": "list_concat",
            "expensive_calls": "memoization",
            "high_freq_io": "buffered_io",
        }

        # Intent‑aware rules for nested loops (snake_case outward)
        self.nested_loop_rules = {
            "membership": "separate_chaining_hash_st",
            "sorting": "merge_sort",
            "dfs": "graph_traversal",
            "generic": "pruning",
        }

    def decide_algorithm(
        self, pattern: str, intent: Optional[str] = None
    ) -> Optional[str]:
        """Return the recommended algorithm identifier (snake_case).

        Args:
            pattern (str):
                Detected performance pattern identifier.
            intent (Optional[str]):
                Developer intent extracted from AST heuristics. Relevant only
                for nested‑loop patterns. Examples include:
                `"membership"`, `"sorting"`, `"dfs"`, `"generic"`.

        Returns:
            Optional[str]:
                Snake_case algorithm identifier, or None if no mapping exists.
        """
        if pattern == "nested_loops":
            if intent:
                return self.nested_loop_rules.get(intent, "pruning")
            return "pruning"

        return self.rule_map.get(pattern)

    def decide_metadata(self, algorithm: str) -> Optional[dict]:
        """Retrieve metadata for a recommended algorithm.

        Args:
            algorithm (str):
                Snake_case algorithm identifier returned by `decide_algorithm`.
                If a caller passes a non‑canonical identifier, it is normalized
                to snake_case before lookup.

        Returns:
            Optional[dict]:
                Metadata dictionary for the algorithm, or None if not found.
        """
        algo_key = algorithm.lower()

        # Normalize PascalCase → snake_case if needed
        if algo_key not in self.metadata:
            # Example: "MergeSort" → "merge_sort"
            normalized = []
            for c in algorithm:
                if c.isupper() and normalized:
                    normalized.append("_")
                normalized.append(c.lower())
            algo_key = "".join(normalized)

        return self.metadata.get(algo_key)

    def decide_fix(self, pattern: str, intent: Optional[str] = None) -> Optional[str]:
        """Return a human‑readable fix recommendation.

        Args:
            pattern (str):
                Detected performance pattern.
            intent (Optional[str]):
                Developer intent for nested loops.

        Returns:
            Optional[str]:
                Short prescriptive recommendation string, or None.
        """
        algo = self.decide_algorithm(pattern, intent)
        if algo:
            return f"Use {algo} to reduce complexity."
        return None

    def decide(self, pattern: str, intent: Optional[str] = None) -> Optional[str]:
        """Primary OSS entrypoint for algorithm selection.

        Args:
            pattern (str):
                Detected performance pattern.
            intent (Optional[str]):
                Developer intent for nested loops.

        Returns:
            Optional[str]:
                Snake_case recommended algorithm identifier.
        """
        return self.decide_algorithm(pattern, intent)
