"""
Alnoms Sorting Algorithms.

Provides a curated collection of comparison‑based sorting algorithms used
throughout the Alnoms DSA suite. Each implementation emphasizes
predictable behavior, clarity, and suitability for visualization and
benchmarking. All algorithms expose a unified interface with optional
step‑by‑step visualization.

Available Algorithms:
- BubbleSort: Adjacent‑swap sorting with early termination.
- InsertionSort: Incremental, stable sorting ideal for small or nearly sorted inputs.
- MergeSort: Stable divide‑and‑conquer sorting with O(N) auxiliary space.
- QuickSort: 3‑way partitioning Quicksort for general‑purpose sorting.
- SelectionSort: Deterministic O(N²) selection‑based sorting.

This module exposes the primary sorting classes for convenient import.
"""

from .bubble_sort import BubbleSort
from .insertion_sort import InsertionSort
from .merge_sort import MergeSort
from .quick_sort import QuickSort
from .selection_sort import SelectionSort

__all__ = [
    "BubbleSort",
    "InsertionSort",
    "MergeSort",
    "QuickSort",
    "SelectionSort",
]
