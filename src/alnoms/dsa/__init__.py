"""
Alnoms DSA Package.

Exposes the public API for the Alnoms Algorithmic Pharmacy, including the
central MetadataRegistry and the curated collections of algorithms and
data‑structure implementations. This package forms the foundation of the
governance‑aware algorithm selection pipeline used by the DecisionEngine.

Responsibilities:
    • Provide the authoritative metadata registry for all algorithms
      (OSS, Pro, and Enterprise tiers)
    • Expose algorithm implementations for benchmarking, education, and
      static/dynamic remediation workflows
    • Expose data‑structure implementations used across detectors, fixers,
      and empirical scaling tests
    • Serve as the integration surface for tiered algorithm extensions

The modules exported here are intentionally deterministic, dependency‑light,
and designed for reproducible research, teaching, and OSS‑tier governance.
"""

from .metadata import MetadataRegistry
from . import algorithms
from . import structures

__all__ = ["MetadataRegistry", "algorithms", "structures"]
