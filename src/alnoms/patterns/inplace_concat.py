"""
Alnoms Detector: In-Place Concatenation.

Identifies Python-specific memory allocation risks that lead to O(N^2)
behavior when using in-place string or list concatenation inside loops.
"""

import ast
from typing import List, Dict, Any
from .base import PatternDetector


class InplaceConcatDetector(PatternDetector):
    """Detects in-place string/list concatenation inside loops.

    This detector identifies patterns where `+=` or `*=` are used on
    potentially non-numeric variables inside `for` or `while` loops.
    Such operations can trigger repeated memory reallocations, resulting
    in O(N^2) scaling.

    The detector includes heuristics to avoid false positives on numeric
    accumulation patterns (e.g., counters, totals, index updates).
    """

    id = "inplace_concat"
    name = "In-Place Concatenation Detection"
    description = "Detects memory-heavy string or list concatenation inside loops."

    NUMERIC_HINTS = {
        "i",
        "j",
        "k",
        "n",
        "m",
        "idx",
        "count",
        "total",
        "sum",
        "acc",
        "value",
    }

    def _looks_numeric(self, node: ast.AST) -> bool:
        """Determines whether an AST node represents numeric-like intent.

        This heuristic helps avoid false positives by identifying RHS
        expressions that are likely numeric accumulations rather than
        string/list concatenations.

        Args:
            node (ast.AST): The AST node representing the right-hand side
                of an augmented assignment.

        Returns:
            bool: True if the node appears numeric (literal number,
            multiplication, or numeric-like variable name). False otherwise.
        """
        # Literal number
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return True

        # RHS contains multiplication → numeric accumulation
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
            return True

        # RHS is a variable with numeric-like name
        if isinstance(node, ast.Name) and node.id.lower() in self.NUMERIC_HINTS:
            return True

        return False

    def detect(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Detects in-place concatenation patterns inside loops.

        Traverses the AST to find augmented assignments (`+=`, `*=`) that
        occur within `for` or `while` loops. The detector filters out
        numeric accumulation patterns and flags only those operations that
        are likely to cause O(N^2) memory behavior due to repeated
        reallocation of strings or lists.

        Args:
            tree (ast.AST): The parsed AST of the target Python module or
                function.

        Returns:
            List[Dict[str, Any]]: A list of findings, where each finding
            includes:
                - function (str): Name of the function containing the issue.
                - pattern_id (str): Identifier for this detector.
                - issue (str): Human-readable description of the problem.
                - complexity (str): Complexity classification.
                - suggestion (str): Recommended remediation strategy.
                - line (int): Line number where the issue occurs.
        """
        findings = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                loops = [
                    c for c in ast.walk(node) if isinstance(c, (ast.For, ast.While))
                ]

                for loop in loops:
                    for child in ast.walk(loop):
                        # Detect += or *=
                        if isinstance(child, ast.AugAssign) and isinstance(
                            child.op, (ast.Add, ast.Mult)
                        ):
                            target = child.target
                            value = child.value

                            # -----------------------------------------------------
                            # 1. Skip numeric accumulation (LHS or RHS numeric)
                            # -----------------------------------------------------
                            # Case: C[i][j] += ...
                            if isinstance(target, ast.Subscript):
                                continue

                            # Case: RHS looks numeric
                            if self._looks_numeric(value):
                                continue

                            # Case: LHS variable name suggests numeric intent
                            if (
                                isinstance(target, ast.Name)
                                and target.id.lower() in self.NUMERIC_HINTS
                            ):
                                continue

                            # -----------------------------------------------------
                            # 2. Detect REAL concatenation
                            # -----------------------------------------------------
                            # Case: literal string/list on RHS
                            if isinstance(
                                value,
                                (ast.List, ast.Tuple, ast.Constant, ast.JoinedStr),
                            ):
                                pass  # real concatenation

                            # Case: variable on LHS that is not numeric-like
                            elif (
                                isinstance(target, ast.Name)
                                and target.id.lower() not in self.NUMERIC_HINTS
                            ):
                                pass

                            else:
                                # Not enough evidence → skip
                                continue

                            # -----------------------------------------------------
                            # 3. Record finding
                            # -----------------------------------------------------
                            findings.append(
                                {
                                    "function": node.name,
                                    "pattern_id": self.id,
                                    "issue": "In-place concatenation inside loop",
                                    "complexity": "O(N^2) Memory Risk",
                                    "suggestion": (
                                        "Collect items in a list and use ''.join() or list.extend() "
                                        "for linear building."
                                    ),
                                    "line": child.lineno,
                                }
                            )

        return findings
