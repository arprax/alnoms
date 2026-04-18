"""
Alnoms Detector: Nested Loops.

Identifies O(N^2) polynomial time complexity risks caused by stacked loops.
Provides lightweight intent classification to support pattern‑specific
remediation in the fixer layer.
"""

import ast
from typing import List, Dict, Any
from .base import PatternDetector


class NestedLoopDetector(PatternDetector):
    """Detects nested loops and classifies their algorithmic intent.

    This detector identifies functions containing nested `for` or `while`
    loops and applies lightweight heuristics to infer the likely purpose
    of the nested structure. The intent classification enables downstream
    fixers to provide context‑aware remediation strategies.

    Supported intent categories:
        • **membership** — equality checks, membership tests, pairwise scans
        • **sorting** — range(len(...)) patterns resembling selection/bubble sort
        • **dfs** — nested iteration over adjacency lists or graph structures
        • **generic** — fallback for unclassified quadratic scans
    """

    id = "nested_loops"
    name = "Nested Loop Detection"
    description = "Detects loops nested inside other loops."

    def _classify_intent(self, loop: ast.AST) -> str:
        """Infers the likely algorithmic intent of a nested loop.

        This heuristic inspects the body of a loop to detect common
        patterns associated with membership checks, sorting‑like scans,
        or DFS‑style neighbor traversal. If no recognizable pattern is
        found, the loop is classified as ``generic``.

        Args:
            loop (ast.AST): The AST node representing the outer loop.

        Returns:
            str: One of ``"membership"``, ``"sorting"``, ``"dfs"``, or
            ``"generic"``.
        """
        for child in ast.walk(loop):
            # Membership / equality checks
            if isinstance(child, ast.Compare):
                for op in child.ops:
                    if isinstance(op, (ast.Eq, ast.In, ast.NotIn)):
                        return "membership"

            # Sorting-like: range(len(...))
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                if child.func.id == "range":
                    for arg in child.args:
                        if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name):
                            if arg.func.id == "len":
                                return "sorting"

            # DFS-like: adjacency traversal
            if isinstance(child, ast.Name) and child.id.lower() in {
                "neighbors",
                "adj",
                "graph",
            }:
                return "dfs"

        return "generic"

    def detect(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Detects nested loops within function bodies.

        Traverses the AST to locate functions containing nested ``for`` or
        ``while`` loops. When a nested loop is found, the detector assigns
        an intent classification and records a single finding per function
        to avoid noise.

        Args:
            tree (ast.AST): The parsed AST of the module being analyzed.

        Returns:
            List[Dict[str, Any]]: A list of findings, where each finding
            includes:
                - function (str): Name of the function containing the loop.
                - pattern_id (str): Identifier for this detector.
                - issue (str): Human-readable description of the problem.
                - complexity (str): Complexity classification (always O(N^2)).
                - intent (str): Classified nested-loop intent.
                - suggestion (str): Guidance for remediation.
                - line (int): Line number of the outer loop.
        """
        findings = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                loops = [
                    c for c in ast.walk(node) if isinstance(c, (ast.For, ast.While))
                ]

                for loop in loops:
                    sub_loops = [
                        c
                        for c in ast.walk(loop)
                        if isinstance(c, (ast.For, ast.While)) and c is not loop
                    ]

                    if sub_loops:
                        intent = self._classify_intent(loop)

                        findings.append(
                            {
                                "function": node.name,
                                "pattern_id": self.id,
                                "issue": "Nested loop detected",
                                "complexity": "O(N^2)",
                                "intent": intent,
                                "suggestion": (
                                    "Nested loop detected; see fixer for pattern-specific remediation."
                                ),
                                "line": loop.lineno,
                            }
                        )
                        break  # one finding per function

        return findings
