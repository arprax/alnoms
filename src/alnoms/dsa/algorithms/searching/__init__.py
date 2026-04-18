"""
Alnoms Searching Algorithms.

Provides classic searching utilities used throughout the Alnoms DSA
suite. These implementations emphasize predictable complexity,
deterministic behavior, and suitability for algorithmic education and
benchmarking. All search routines assume the input list is sorted unless
otherwise specified.

Available Algorithms:
- BinarySearch: Exact‑match search and rank computation in O(log N) time.

This module exposes the primary searching utilities for convenient import.
"""

from .binary_search import BinarySearch

__all__ = ["BinarySearch"]
