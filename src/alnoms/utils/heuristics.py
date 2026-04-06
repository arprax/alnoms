"""
Alnoms: Static Code Heuristics Engine.

This module provides Abstract Syntax Tree (AST) analysis for the Alnoms
Pre-Deployment Governance framework. It performs structural audits on Python
source code to identify algorithmic anti-patterns and performance regressions
without executing the code.

The engine targets the 'Top 6' killers of Python performance, including
high-complexity loops, redundant sorting, and high-frequency system calls.
"""

import ast
from typing import List, Dict, Any


class CodeAnalyzer(ast.NodeVisitor):
    """
    AST NodeVisitor designed to audit Python functions for scaling risks.

    By traversing the function's syntax tree, this class identifies structural
    patterns that lead to non-linear execution time (O(N^2) or worse) or
    unnecessary resource contention.
    """

    def __init__(self):
        """Initializes a new analyzer with an empty list of governance issues."""
        self.issues: List[Dict[str, Any]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        Interrogates a function definition to identify performance anti-patterns.

        This method acts as the primary auditor, running six distinct logic gates
        to detect structural inefficiencies.

        Args:
            node (ast.FunctionDef): The AST node representing the function to be audited.
        """
        # 1. Scope Identification: Locate all loops (For/While) within the function
        loops = [
            child for child in ast.walk(node) if isinstance(child, (ast.For, ast.While))
        ]

        # 2. NESTED LOOP DETECTION (O(N^2) Risk)
        # Logic: Scans the internal body of every detected loop for a secondary loop.
        # This identifies polynomial complexity where search-and-match operations
        # should likely be replaced with Hashmaps.
        for loop in loops:
            sub_loops = [
                c
                for c in ast.walk(loop)
                if isinstance(c, (ast.For, ast.While)) and c is not loop
            ]
            if sub_loops:
                self.issues.append(
                    {
                        "function": node.name,
                        "issue": "Nested loop detected",
                        "complexity": "O(N^2)",
                        "suggestion": "Use a hashmap (dict) or set to reduce complexity from O(N^2) to O(N).",
                    }
                )
                break  # Flag once per function to prevent terminal noise

        # Define performance-sensitive function sets
        # Safe built-ins are O(1) or safe for use in high-frequency loops
        safe_builtins = {
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
            "append",
        }
        sorting_funcs = {"sort", "sorted"}
        io_funcs = {"open", "read", "write", "print"}

        for loop in loops:
            for child in ast.walk(loop):
                # 3. EXPENSIVE CALL & REDUNDANT SORTING DETECTION
                # Logic: Inspects all ast.Call nodes to identify non-linear or redundant logic.
                if isinstance(child, ast.Call):
                    func_name = ""
                    if isinstance(child.func, ast.Name):
                        func_name = child.func.id
                    elif isinstance(child.func, ast.Attribute):
                        func_name = child.func.attr

                    # Redundant Sorting Logic: O(N * N log N) risk
                    if func_name in sorting_funcs:
                        self.issues.append(
                            {
                                "function": node.name,
                                "issue": "Redundant sorting inside loop",
                                "complexity": "O(N^2 log N)",
                                "suggestion": "Move sorting logic outside the loop to sort data only once.",
                            }
                        )

                    # General Expensive Call Detection
                    elif func_name and func_name not in safe_builtins:
                        self.issues.append(
                            {
                                "function": node.name,
                                "issue": f"Expensive call to '{func_name}()' inside loop",
                                "complexity": "O(N * K)",
                                "suggestion": "Hoist the function call or cache its results to avoid repeated execution.",
                            }
                        )

                    # 4. HIGH-FREQUENCY I/O DETECTION
                    # Logic: Detects system calls (open/read/write) that incur massive context-switching
                    # overhead when placed inside tight loops.
                    if func_name in io_funcs:
                        self.issues.append(
                            {
                                "function": node.name,
                                "issue": "High-frequency I/O inside loop",
                                "complexity": "High I/O Wait",
                                "suggestion": "Buffer data in memory and perform a single batch I/O operation outside the loop.",
                            }
                        )

                # 5. IN-PLACE CONCATENATION (O(N^2) Building)
                # Logic: Detects '+=' or '*=' on variables inside loops, which often creates
                # new objects in memory for every iteration in Python.
                if isinstance(child, ast.AugAssign) and isinstance(
                    child.op, (ast.Add, ast.Mult)
                ):
                    self.issues.append(
                        {
                            "function": node.name,
                            "issue": "In-place concatenation inside loop",
                            "complexity": "O(N^2) Memory Risk",
                            "suggestion": "Collect items in a list and use ''.join() or list.extend() for linear building.",
                        }
                    )

        self.generic_visit(node)


def analyze_code(path: str) -> List[Dict[str, Any]]:
    """
    Parses a Python file into an AST and executes the Alnoms governance audit.

    This function serves as the entry point for static analysis, providing
    resilience against encoding errors and syntax failures.

    Args:
        path (str): The file system path to the target Python script.

    Returns:
        List[Dict[str, Any]]: A collection of detected governance violations
            containing the function name, issue description, and remediation.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()
            if not source.strip():
                return []
            tree = ast.parse(source)

        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        return analyzer.issues
    except Exception as e:
        # Graceful failure for syntax or I/O errors ensures CLI stability
        return [
            {
                "function": "file_level",
                "issue": f"AST Analysis Error: {str(e)}",
                "complexity": "Unknown",
                "suggestion": "Check file syntax or encoding",
            }
        ]
