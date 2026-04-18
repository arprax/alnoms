"""
Alnoms Core.

Defines the primary execution, orchestration, and governance components of
the Alnoms framework. This package exposes the public API for profiling,
static analysis, algorithm selection, data generation, and I/O utilities.

Subsystem Responsibilities:
    • Execution & orchestration engine (ScriptAnalyzer)
    • Deterministic performance profiling (Profiler)
    • Rule‑based algorithm selection (DecisionEngine)
    • Synthetic dataset generation for benchmarking (DataGenerator)
    • Standardized input loading utilities (DataReader)

The modules exported here form the backbone of the OSS‑tier optimization
and pre‑deployment governance pipeline. They are intentionally deterministic,
side‑effect‑free, and designed for reproducible research and CI‑safe usage.
"""

from .profiler import Profiler
from .analyzer import ScriptAnalyzer
from .decision_engine import DecisionEngine
from .generators import DataGenerator
from .io import DataReader

__all__ = [
    "Profiler",
    "ScriptAnalyzer",
    "DecisionEngine",
    "DataGenerator",
    "DataReader",
]
