"""
Alnoms Pattern Registry.

Defines the public API for the Alnoms static analysis subsystem. This
package exposes the HeuristicsEngine, the open‑core pattern registry, and
the canonical `analyze_code()` entrypoint used throughout the governance
pipeline.

Responsibilities:
    • Provide a stable interface for AST‑based pattern detection
    • Expose the registry of all OSS‑tier pattern detectors
    • Lift `analyze_code()` for consumption by the orchestration engine
    • Serve as the integration surface for PRO/Enterprise detectors when
      dynamically injected via sovereign extension loading

The registry and engine defined here form the foundation of Alnoms'
static analysis layer, enabling loop‑depth inference, anti‑pattern
detection, and metadata‑driven remediation workflows.
"""

from .heuristics import HeuristicsEngine, REGISTRY, get_registered_patterns

# Lifting the entry point for alnoms.core.analyzer
analyze_code = HeuristicsEngine.analyze_code

__all__ = ["analyze_code", "HeuristicsEngine", "REGISTRY", "get_registered_patterns"]
