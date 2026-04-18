"""
Alnoms DSA Algorithms.

Provides a curated collection of algorithmic modules forming the
"Complexity Canon" of the Alnoms ecosystem. These modules implement
canonical algorithms across sorting, searching, graph processing, and
pointer‑based techniques. All implementations emphasize clarity,
predictable complexity, and suitability for benchmarking and education.

Available Submodules:
- sorting: Comparison‑based and non‑comparison sorting algorithms.
- searching: Classic search routines and symbol‑table helpers.
- graph: Foundational graph algorithms and traversals.
- pointers: Pointer‑based algorithmic patterns and utilities.

This package exposes the primary algorithm modules for convenient import.
"""

from . import sorting
from . import searching
from . import graph
from . import pointers

__all__ = ["sorting", "searching", "graph", "pointers"]
