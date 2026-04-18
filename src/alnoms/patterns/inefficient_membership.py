"""
Alnoms Detector: Inefficient Membership Testing.

Identifies hidden O(N) membership scans inside loops, which can silently
produce O(N²) behavior when the target container is a list or tuple.
This detector applies heuristics to avoid false positives on sets, dicts,
ranges, and variables whose names imply O(1) membership semantics.
"""

import ast
from typing import List, Dict, Any
from .base import PatternDetector


class MembershipDetector(PatternDetector):
    """Detect inefficient membership tests inside loops.

    This detector flags occurrences of:

        - `x in some_list`
        - `x not in some_list`
        - membership checks on literal lists/tuples
        - membership checks on variables that are likely lists

    When these appear inside loops, they create a hidden O(N²) pattern due to
    repeated linear scans. The detector uses heuristics to avoid false positives
    on safe containers such as sets, dicts, ranges, and variables whose names
    imply O(1) lookup semantics (e.g., `visited`, `cache`, `lookup`).

    Attributes:
        SAFE_CONTAINER_HINTS (set[str]):
            Variable‑name substrings that imply O(1) membership semantics.
    """

    id = "inefficient_membership"
    name = "Inefficient Membership Detection"
    description = "Detects 'in' operator usage on list-like containers inside loops."

    SAFE_CONTAINER_HINTS = {
        "set",
        "dict",
        "map",
        "cache",
        "visited",
        "seen",
        "lookup",
        "index",
    }

    def _is_safe_container_name(self, name: str) -> bool:
        """Return True if the variable name implies O(1) membership.

        Args:
            name (str): Variable name extracted from the AST.

        Returns:
            bool: True if the name suggests a set/dict‑like container.
        """
        name = name.lower()
        return any(hint in name for hint in self.SAFE_CONTAINER_HINTS)

    def detect(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze the AST and flag inefficient membership tests inside loops.

        Args:
            tree (ast.AST): Parsed AST of the target Python file.

        Returns:
            List[Dict[str, Any]]:
                A list of findings. Each finding includes:
                    - "function": Function where the issue occurs
                    - "pattern_id": Identifier for this detector
                    - "issue": Description of the membership test
                    - "complexity": Estimated complexity impact
                    - "suggestion": Recommended remediation
                    - "line": Line number of the issue

        Notes:
            - Literal lists/tuples of size ≤ 3 are ignored as they are cheap.
            - Safe containers (set/dict/range) are skipped.
            - Variable names are heuristically classified for safety.
        """
        findings = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                loops = [
                    c for c in ast.walk(node) if isinstance(c, (ast.For, ast.While))
                ]

                for loop in loops:
                    for child in ast.walk(loop):
                        # Look for "x in Y" or "x not in Y"
                        if isinstance(child, ast.Compare):
                            for op in child.ops:
                                if isinstance(op, (ast.In, ast.NotIn)):
                                    container = child.comparators[0]

                                    # --- CASE 1: Literal list/tuple ---
                                    if isinstance(container, (ast.List, ast.Tuple)):
                                        # Ignore tiny constant lists (<= 3)
                                        if len(container.elts) <= 3:
                                            continue

                                        findings.append(
                                            {
                                                "function": node.name,
                                                "pattern_id": self.id,
                                                "issue": (
                                                    "Membership test on list literal "
                                                    "inside loop"
                                                ),
                                                "complexity": "Potential O(N^2)",
                                                "suggestion": (
                                                    "Convert the list literal to a set "
                                                    "for O(1) lookups."
                                                ),
                                                "line": child.lineno,
                                            }
                                        )
                                        continue

                                    # --- CASE 2: Variable name ---
                                    if isinstance(container, ast.Name):
                                        var_name = container.id

                                        # Skip safe containers by name
                                        if self._is_safe_container_name(var_name):
                                            continue

                                        findings.append(
                                            {
                                                "function": node.name,
                                                "pattern_id": self.id,
                                                "issue": (
                                                    f"Membership test ('in {var_name}') "
                                                    "inside loop"
                                                ),
                                                "complexity": "Potential O(N^2)",
                                                "suggestion": (
                                                    f"Ensure '{var_name}' is a Set or Dict "
                                                    "for O(1) lookups, not a List."
                                                ),
                                                "line": child.lineno,
                                            }
                                        )
                                        continue

                                    # --- CASE 3: Calls like set(...), dict(...), range(...) ---
                                    if isinstance(container, ast.Call):
                                        if isinstance(container.func, ast.Name):
                                            if container.func.id in {
                                                "set",
                                                "dict",
                                                "range",
                                            }:
                                                continue  # safe

                                    # --- DEFAULT: Unknown container type ---
                                    findings.append(
                                        {
                                            "function": node.name,
                                            "pattern_id": self.id,
                                            "issue": "Membership test inside loop",
                                            "complexity": "Potential O(N^2)",
                                            "suggestion": (
                                                "Ensure the target collection is a Set or Dict."
                                            ),
                                            "line": child.lineno,
                                        }
                                    )

        return findings
