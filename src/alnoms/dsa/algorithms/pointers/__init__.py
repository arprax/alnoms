"""
Alnoms Pointer Algorithms.

Provides classic pointer‑based algorithmic utilities, including
fast/slow traversal patterns and linked‑list cycle detection. These
algorithms emphasize constant‑space operations and are foundational in
linked‑list processing, interview‑style problems, and low‑level data
structure manipulation.

Available Algorithms:
- CycleDetector: Floyd’s Tortoise‑and‑Hare cycle detection.

This module exposes the primary pointer utilities for convenient import.
"""

from .cycle_detector import CycleDetector

__all__ = ["CycleDetector"]
