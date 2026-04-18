"""
Alnoms Fixer Registry.

Central registry for all OSS‑tier fixers and dynamic extension loaders for
Pro and Enterprise tiers. This module defines the authoritative mapping
between detected performance patterns and their corresponding remediation
strategies.

Responsibilities:
    • Register all open‑core (Tier 0) fixers
    • Dynamically load Pro (Tier 1/2) and Enterprise (Tier 3) fixers when
      license keys are present
    • Provide O(1) lookup for fixers by pattern ID
    • Expose a stable public API for the remediation subsystem

Open‑core fixers provide:
    • Human‑readable explanations
    • Before/after code snippets
    • Qualitative cost‑shift estimates
    • Cure‑type classification

Commercial tiers override:
    • generate_patch() — enabling automated refactoring
    • is_safe_to_apply() — enabling safe auto‑application
    • multi‑file and PR‑generation workflows

This registry is intentionally deterministic and side‑effect‑free unless
commercial extensions are explicitly enabled via environment variables.
"""

from typing import List, Dict, Optional
import os

from .base import Fixer

# ---------------------------------------------------------
# Import the 6 Open Core Fixers (Tier 0 – OSS)
# ---------------------------------------------------------
from .nested_loops_fixer import NestedLoopFixer
from .redundant_sort_fixer import RedundantSortFixer
from .expensive_calls_fixer import ExpensiveCallFixer
from .high_freq_io_fixer import HighFrequencyIOFixer
from .inplace_concat_fixer import InplaceConcatFixer
from .inefficient_membership_fixer import InefficientMembershipFixer

# ---------------------------------------------------------
# OPEN CORE REGISTRY
# ---------------------------------------------------------
REGISTRY: List[Fixer] = [
    NestedLoopFixer(),
    RedundantSortFixer(),
    ExpensiveCallFixer(),
    HighFrequencyIOFixer(),
    InplaceConcatFixer(),
    InefficientMembershipFixer(),
]


# ---------------------------------------------------------
# Feature flag helpers
# ---------------------------------------------------------
def _pro_enabled() -> bool:
    """Return True if Pro‑tier fixers should be loaded."""
    return os.getenv("ALNOMS_PRO_KEY") not in (None, "")


def _enterprise_enabled() -> bool:
    """Return True if Enterprise‑tier fixers should be loaded."""
    return os.getenv("ALNOMS_ENTERPRISE_KEY") not in (None, "")


# ---------------------------------------------------------
# Sovereign Extension Loader (Tier 1/2/3 – Paid)
# ---------------------------------------------------------
if _pro_enabled():
    try:
        from alnoms_pro.fixes import PRO_FIXERS

        REGISTRY.extend(PRO_FIXERS)
    except ImportError:
        pass

if _enterprise_enabled():
    try:
        from alnoms_enterprise.fixes import ENTERPRISE_FIXERS

        REGISTRY.extend(ENTERPRISE_FIXERS)
    except ImportError:
        pass


# ---------------------------------------------------------
# Public API & Routing
# ---------------------------------------------------------
def get_registered_fixers() -> List[Fixer]:
    """Return all active fixers, including dynamically loaded extensions."""
    return REGISTRY


# Build a fast O(1) lookup map dynamically based on whatever is registered
_FIXER_MAP: Dict[str, Fixer] = {fixer.pattern_id: fixer for fixer in REGISTRY}


def get_fixer(pattern_id: str) -> Optional[Fixer]:
    """
    Retrieve the fixer associated with a given pattern ID.

    Args:
        pattern_id (str): Identifier of the detected performance pattern.

    Returns:
        Optional[Fixer]: The corresponding fixer instance, or None if no
        fixer is registered for the given pattern.
    """
    return _FIXER_MAP.get(pattern_id)
