"""
Alnoms Detector: Redundant Sorting.

Identifies O(N^2 log N) performance degradation caused by invoking Python's
sorting operations inside loops. Sorting should generally occur once,
outside the loop body, to avoid repeated O(N log N) work.
"""

import ast
from typing import List, Dict, Any
from .base import PatternDetector


class RedundantSortDetector(PatternDetector):
    """Detects repeated sorting operations executed inside loops.

    This detector inspects loop bodies for calls to Python's built‑in
    sorting mechanisms (`sorted()` or list `.sort()`). When these calls
    appear inside `for` or `while` loops, they can introduce
    O(N^2 log N) behavior due to repeated sorting of the same or similar
    data structures.

    Sorting is typically intended to be performed once before iteration,
    or once after data collection, rather than on every loop iteration.
    """

    id = "redundant_sort"
    name = "Redundant Sort Detection"
    description = "Detects sorting operations executed inside loops."

    def detect(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Detects sorting calls (`sort`, `sorted`) inside loop bodies.

        Traverses the AST to locate function definitions and inspects all
        nested loops for calls to Python's standard sorting functions.
        When found, the detector records a finding indicating that sorting
        should be moved outside the loop to avoid repeated O(N log N)
        operations.

        Args:
            tree (ast.AST): The parsed AST of the module being analyzed.

        Returns:
            List[Dict[str, Any]]: A list of findings, where each finding
            includes:
                - function (str): Name of the function containing the issue.
                - pattern_id (str): Identifier for this detector.
                - issue (str): Description of the redundant sorting pattern.
                - complexity (str): Complexity classification (O(N^2 log N)).
                - suggestion (str): Recommended remediation strategy.
                - line (int): Line number where the sorting call occurs.
        """
        findings = []
        sorting_funcs = {"sort", "sorted"}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                loops = [
                    c for c in ast.walk(node) if isinstance(c, (ast.For, ast.While))
                ]

                for loop in loops:
                    for child in ast.walk(loop):
                        if isinstance(child, ast.Call):
                            func_name = ""

                            # Case: sorted(...)
                            if isinstance(child.func, ast.Name):
                                func_name = child.func.id

                            # Case: list.sort(...)
                            elif isinstance(child.func, ast.Attribute):
                                func_name = child.func.attr

                            if func_name in sorting_funcs:
                                findings.append(
                                    {
                                        "function": node.name,
                                        "pattern_id": self.id,
                                        "issue": "Redundant sorting inside loop",
                                        "complexity": "O(N^2 log N)",
                                        "suggestion": (
                                            "Move sorting logic outside the loop to sort data only once."
                                        ),
                                        "line": child.lineno,
                                    }
                                )

        return findings
