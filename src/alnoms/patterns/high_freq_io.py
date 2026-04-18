"""
Alnoms Detector: High‑Frequency I/O.

Identifies file or network I/O operations placed inside tight loops. These
operations incur significant OS‑level overhead due to system calls, kernel
context switching, and disk/network latency. The detector flags such patterns
and recommends buffering or batching strategies.
"""

import ast
from typing import List, Dict, Any
from .base import PatternDetector


class HighFrequencyIODetector(PatternDetector):
    """Detect high‑frequency I/O operations inside loops.

    This detector walks the AST of each function and inspects all `for` and
    `while` loops. Any call to `open`, `read`, or `write` inside a loop is
    flagged as a performance risk due to:

    - Excessive system calls
    - Kernel context switching
    - Disk or network latency
    - Reduced throughput compared to buffered operations

    Attributes:
        id (str): Unique identifier for this detector.
        name (str): Human‑readable name for reporting.
        description (str): Short description of the detector's purpose.
    """

    id = "high_freq_io"
    name = "High-Frequency I/O Detection"
    description = "Detects file or network I/O operations inside loops."

    def detect(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze the AST and flag I/O operations inside loops.

        Args:
            tree (ast.AST): Parsed AST of the target Python file.

        Returns:
            List[Dict[str, Any]]:
                A list of findings. Each finding includes:
                    - "function": Name of the function containing the loop.
                    - "pattern_id": Identifier for this detector.
                    - "issue": Description of the detected I/O call.
                    - "complexity": Qualitative complexity impact.
                    - "suggestion": Recommended remediation.
                    - "line": Line number of the call.

        Notes:
            - Only explicit `ast.Call` nodes inside `for`/`while` loops are inspected.
            - This detector focuses on file and network I/O primitives.
            - Buffered or batched I/O is recommended for performance.
        """
        findings = []
        io_funcs = {"open", "read", "write"}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                loops = [
                    c for c in ast.walk(node) if isinstance(c, (ast.For, ast.While))
                ]

                for loop in loops:
                    for child in ast.walk(loop):
                        if isinstance(child, ast.Call):
                            func_name = ""
                            if isinstance(child.func, ast.Name):
                                func_name = child.func.id
                            elif isinstance(child.func, ast.Attribute):
                                func_name = child.func.attr

                            if func_name in io_funcs:
                                findings.append(
                                    {
                                        "function": node.name,
                                        "pattern_id": self.id,
                                        "issue": (
                                            f"High-frequency I/O ('{func_name}') inside loop"
                                        ),
                                        "complexity": "High I/O Wait",
                                        "suggestion": (
                                            "Buffer data in memory and perform a single "
                                            "batch I/O operation outside the loop."
                                        ),
                                        "line": child.lineno,
                                    }
                                )

        return findings
