"""
Alnoms: Pattern Detection Interface.

Defines the abstract contract for static analysis detectors. This modular
architecture enables the Alnoms engine to be extended with custom heuristic
rules for identifying algorithmic anti‑patterns in Python ASTs.
"""

import ast
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class PatternDetector(ABC):
    """Abstract base class for all Alnoms static pattern detectors.

    Each detector implements a specific heuristic for identifying performance
    risks or algorithmic anti‑patterns in Python source code. Detectors operate
    on the parsed Abstract Syntax Tree (AST) and return structured findings
    describing the issue, its location, and any relevant metadata.

    Attributes:
        id (str): Unique identifier for the detector.
        name (str): Human‑readable name for reporting.
        description (str): Short description of the detector's purpose.
    """

    # Metadata for reporting and governance tiering
    id: str = "base_detector"
    name: str = "Abstract Base Detector"
    description: str = "Base interface for static heuristic analysis."

    @abstractmethod
    def detect(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze a Python AST and return pattern‑specific findings.

        Subclasses must implement this method to walk the AST and identify
        occurrences of the pattern they are responsible for detecting.

        Args:
            tree (ast.AST): The parsed AST of the target Python file.

        Returns:
            List[Dict[str, Any]]:
                A list of findings. Each finding is a dictionary containing:
                    - "function": Name of the function where the issue occurs.
                    - "pattern_id": Identifier of the detected pattern.
                    - "line": Line number of the issue.
                    - "message": Human‑readable description of the issue.
                    - Additional detector‑specific metadata.

        Notes:
            - Detectors should not modify the AST.
            - Detectors should avoid raising exceptions; they must fail gracefully.
        """
        pass
