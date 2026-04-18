"""
Alnoms: Static Code Heuristics Engine.

Provides a modular, extensible framework for AST‑based static analysis.
This engine dispatches the parsed Python AST to a registry of specialized
pattern detectors, each responsible for identifying a specific class of
algorithmic anti‑patterns.

The engine supports OSS, PRO, and ENTERPRISE tiers through dynamic registry
extension based on environment feature flags.
"""

import ast
import os
from typing import List, Dict, Any

# 1. Internal Imports (Modular Specialists)
from .base import PatternDetector
from .nested_loops import NestedLoopDetector
from .redundant_sort import RedundantSortDetector
from .expensive_calls import ExpensiveCallDetector
from .high_freq_io import HighFrequencyIODetector
from .inplace_concat import InplaceConcatDetector
from .inefficient_membership import MembershipDetector

# 2. Registry Definition (Moved here to prevent circular imports)
REGISTRY: List[PatternDetector] = [
    NestedLoopDetector(),
    RedundantSortDetector(),
    ExpensiveCallDetector(),
    HighFrequencyIODetector(),
    InplaceConcatDetector(),
    MembershipDetector(),
]


# 3. Feature Flag Helpers & Sovereign Loader
def _pro_enabled() -> bool:
    """Return True if PRO‑tier detectors should be enabled.

    Returns:
        bool: True if the environment variable `ALNOMS_PRO_KEY` is set.
    """
    return os.getenv("ALNOMS_PRO_KEY") is not None


def _enterprise_enabled() -> bool:
    """Return True if ENTERPRISE‑tier detectors should be enabled.

    Returns:
        bool: True if the environment variable `ALNOMS_ENTERPRISE_KEY` is set.
    """
    return os.getenv("ALNOMS_ENTERPRISE_KEY") is not None


# Dynamically extend registry with PRO/ENTERPRISE detectors
if _pro_enabled():
    try:
        from alnoms_pro.patterns import PRO_REGISTRY

        REGISTRY.extend(PRO_REGISTRY)
    except ImportError:
        pass

if _enterprise_enabled():
    try:
        from alnoms_enterprise.patterns import ENTERPRISE_REGISTRY

        REGISTRY.extend(ENTERPRISE_REGISTRY)
    except ImportError:
        pass


# 4. The Engine Class
class HeuristicsEngine:
    """Orchestrates AST analysis using the registered pattern detectors.

    The engine loads all OSS detectors by default and conditionally extends
    the registry with PRO and ENTERPRISE detectors based on environment
    feature flags. Each detector is responsible for identifying a specific
    algorithmic anti‑pattern.

    This class exposes a single static method, `analyze_code`, which parses
    the file into an AST and dispatches it to all registered detectors.
    """

    @staticmethod
    def analyze_code(path: str) -> List[Dict[str, Any]]:
        """Analyze a Python file using all registered pattern detectors.

        Args:
            path (str): Path to the Python source file.

        Returns:
            List[Dict[str, Any]]:
                A flat list of findings from all detectors. Each finding is a
                dictionary containing detector‑specific metadata such as:
                    - "function": Function where the issue occurs
                    - "pattern_id": Identifier of the detector
                    - "issue": Description of the anti‑pattern
                    - "line": Line number of the issue
                    - Additional detector‑specific fields

        Notes:
            - Empty files return an empty list.
            - Syntax errors or unexpected exceptions are captured and returned
              as a single file‑level finding rather than raising an exception.
        """
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                source = f.read()
                if not source.strip():
                    return []
                tree = ast.parse(source)

            all_findings = []
            # Dispatch AST to all registered detectors
            for detector in REGISTRY:
                findings = detector.detect(tree)
                all_findings.extend(findings)

            return all_findings

        except Exception as e:
            return [
                {
                    "function": "file_level",
                    "issue": f"Static Analysis Error: {str(e)}",
                    "complexity": "Unknown",
                    "suggestion": "Check file syntax. Empirical tests will proceed.",
                    "line": 0,
                }
            ]


def get_registered_patterns() -> List[PatternDetector]:
    """Return the list of all registered pattern detectors.

    Returns:
        List[PatternDetector]: The active detector registry, including OSS,
        PRO, and ENTERPRISE detectors if enabled.
    """
    return REGISTRY
