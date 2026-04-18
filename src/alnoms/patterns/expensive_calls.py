"""
Alnoms Detector: Expensive Calls.

Identifies non‑trivial function calls inside loops that may compound execution
time. This detector flags calls that are not part of a curated O(1) whitelist,
helping developers identify repeated work inside iterative structures.
"""

import ast
from typing import List, Dict, Any
from .base import PatternDetector


class ExpensiveCallDetector(PatternDetector):
    """Detect potentially expensive function calls inside loops.

    This detector walks the AST of each function and inspects all `for` and
    `while` loops. Any function call inside a loop that is *not* part of the
    `SAFE_CALLS` whitelist is flagged as a potential performance risk.

    The whitelist includes:

    - Common O(1) built‑ins (`len`, `range`, `int`, etc.)
    - Common O(1) container methods (`append`, `pop`, `get`, etc.)
    - Sorting and I/O calls, which are handled by dedicated detectors

    Attributes:
        SAFE_CALLS (set[str]): Set of known O(1) or trivial operations that
            should not be flagged.
    """

    id = "expensive_calls"
    name = "Expensive Call Detection"
    description = "Detects potentially expensive function calls inside loops."

    # --- SAFE CALLS (O(1) or trivial) ---
    SAFE_CALLS = {
        # Builtins
        "range",
        "len",
        "print",
        "enumerate",
        "int",
        "str",
        "float",
        "list",
        "dict",
        "set",
        "tuple",
        # Common O(1) methods
        "append",
        "pop",
        "add",
        "get",
        "update",
        "remove",
        "clear",
        # Sorting is handled by a separate detector
        "sort",
        "sorted",
        # IO is handled separately
        "open",
        "read",
        "write",
    }

    def detect(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze the AST and flag non‑whitelisted calls inside loops.

        Args:
            tree (ast.AST): Parsed AST of the target Python file.

        Returns:
            List[Dict[str, Any]]:
                A list of findings. Each finding includes:
                    - "function": Name of the function containing the loop.
                    - "pattern_id": Identifier for this detector.
                    - "issue": Description of the detected call.
                    - "complexity": Estimated complexity impact.
                    - "suggestion": Recommended remediation.
                    - "line": Line number of the call.

        Notes:
            - Only explicit `ast.Call` nodes inside `for`/`while` loops are inspected.
            - Calls to safe O(1) operations are ignored.
            - Sorting and I/O calls are delegated to other detectors.
        """
        findings = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                loops = [
                    c for c in ast.walk(node) if isinstance(c, (ast.For, ast.While))
                ]

                for loop in loops:
                    for child in ast.walk(loop):
                        if isinstance(child, ast.Call):
                            # Extract function name
                            func_name = ""
                            if isinstance(child.func, ast.Name):
                                func_name = child.func.id
                            elif isinstance(child.func, ast.Attribute):
                                func_name = child.func.attr

                            # Skip safe calls
                            if func_name in self.SAFE_CALLS:
                                continue

                            # Skip empty or unknown names
                            if not func_name:
                                continue

                            # Flag everything else as potentially expensive
                            findings.append(
                                {
                                    "function": node.name,
                                    "pattern_id": self.id,
                                    "issue": (
                                        f"Potentially expensive call '{func_name}()' "
                                        "inside loop"
                                    ),
                                    "complexity": "O(N * K)",
                                    "suggestion": (
                                        "Consider hoisting or caching this call outside "
                                        "the loop to avoid repeated execution."
                                    ),
                                    "line": child.lineno,
                                }
                            )

        return findings
