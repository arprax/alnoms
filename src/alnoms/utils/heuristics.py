"""
Alnoms: Static Code Heuristics Engine.

Provides Abstract Syntax Tree (AST) analysis for the Pre-Deployment Governance framework.
Scans Python source code statically to identify algorithmic anti-patterns and scaling
risks without requiring runtime execution.

Features:
    - Loop Detection: Identifies nested loop structures indicative of O(N^2) complexity.
    - Expensive Call Detection: Flags non-standard or expensive API calls inside loops.
    - Safe Built-in Whitelisting: Ignores O(1) native Python functions to eliminate false positives.
"""

import ast


class CodeAnalyzer(ast.NodeVisitor):
    """
    AST NodeVisitor designed to traverse and audit Python function definitions.
    Identifies structural inefficiencies that indicate poor algorithmic scaling.
    """

    def __init__(self):
        self.issues = []

    def visit_FunctionDef(self, node):
        """
        Intercepts and analyzes function definitions within the AST.

        Evaluates the internal structure of the function to detect:
            1. Nested loops (O(N^2) risk).
            2. Expensive function calls inside loops (O(N * K) risk), filtering out O(1) built-ins.

        Args:
            node (ast.FunctionDef): The AST node representing a function definition.
        """
        # 1. Find all loops (For and While) in the function
        loops = [
            child for child in ast.walk(node) if isinstance(child, (ast.For, ast.While))
        ]

        # 2. Check for actual Nested Loops (a loop inside another loop)
        for loop in loops:
            # Walk the children of this specific loop to see if another loop exists inside it
            sub_loops = [
                child
                for child in ast.walk(loop)
                if isinstance(child, (ast.For, ast.While)) and child is not loop
            ]
            if sub_loops:
                self.issues.append(
                    {
                        "function": node.name,
                        "issue": "Nested loop detected",
                        "complexity": "O(N^2)",
                        "suggestion": "Use a hashmap or set to reduce complexity",
                    }
                )
                break  # Only flag once per function to avoid spamming the terminal

        # 3. Check for Expensive Function Calls Inside Loops
        # We whitelist O(1) or safe Python built-ins so they don't trigger false positives
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

        for loop in loops:
            for child in ast.walk(loop):
                if isinstance(child, ast.Call):
                    if (
                        isinstance(child.func, ast.Name)
                        and child.func.id not in safe_builtins
                    ):
                        self.issues.append(
                            {
                                "function": node.name,
                                "issue": f"Expensive call to '{child.func.id}()' inside loop",
                                "complexity": "O(N * K)",
                                "suggestion": "Cache results or hoist the function call outside the loop",
                            }
                        )
                        break

        self.generic_visit(node)


def analyze_code(path: str) -> list:
    """
    Parses a target Python file into an Abstract Syntax Tree (AST) and runs the static auditor.

    Args:
        path (str): The system path to the target Python script.

    Returns:
        list[dict]: A list of detected governance violations. Each dictionary contains:
                    - function: Name of the offending function.
                    - issue: Description of the detected anti-pattern.
                    - complexity: Estimated Big-O complexity risk.
                    - suggestion: Recommended remediation strategy.
    """
    with open(path, "r") as f:
        tree = ast.parse(f.read())

    analyzer = CodeAnalyzer()
    analyzer.visit(tree)

    return analyzer.issues
