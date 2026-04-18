"""
Alnoms: Public API Surface.

Exposes the primary entrypoints for the Alnoms optimization and governance
framework. This package‑level initializer lifts the core orchestration,
profiling, data‑generation, and algorithm‑selection components into a
single unified namespace for end‑users, notebooks, and CLI integrations.

Responsibilities:
    • Provide a stable, top‑level API for external consumers
    • Re‑export core execution and analysis components
    • Maintain a clean, dependency‑free import surface for OSS usage
    • Serve as the canonical import path for teaching, demos, and research

The symbols exported here represent the foundational building blocks of
the Alnoms pre‑deployment governance pipeline.
"""

from alnoms.core.profiler import Profiler
from alnoms.core.analyzer import ScriptAnalyzer
from alnoms.core.generators import DataGenerator
from alnoms.core.decision_engine import DecisionEngine  # Lifted for Public API

__all__ = ["Profiler", "ScriptAnalyzer", "DataGenerator", "DecisionEngine"]
