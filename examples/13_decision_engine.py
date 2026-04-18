"""
Demo 13: Decision Engine Mapping

Shows how the OSS DecisionEngine maps detected patterns
(and nested-loop intent) to recommended algorithm families.
"""

from alnoms.core.decision_engine import DecisionEngine
from alnoms.dsa.metadata import MetadataRegistry


def demo_decision_engine():
    # Load metadata registry (complexities, notes, stability)
    metadata = MetadataRegistry.get_all()

    # Initialize engine
    engine = DecisionEngine(metadata)

    print("\n=== Decision Engine Demo ===\n")

    # 1. Simple patterns
    patterns = [
        "inefficient_membership",
        "redundant_sort",
        "inplace_concat",
        "expensive_calls",
        "high_freq_io",
    ]

    for p in patterns:
        algo = engine.decide(p)
        meta = engine.decide_metadata(algo)
        print(f"Pattern: {p}")
        print(f"  → Recommended Algorithm: {algo}")
        print(f"  → Metadata: {meta}\n")

    # 2. Nested-loop intent-aware mapping
    intents = ["membership", "sorting", "dfs", "generic"]

    for intent in intents:
        algo = engine.decide("nested_loops", intent=intent)
        meta = engine.decide_metadata(algo)
        print(f"Nested Loop Intent: {intent}")
        print(f"  → Recommended Algorithm: {algo}")
        print(f"  → Metadata: {meta}\n")


if __name__ == "__main__":
    demo_decision_engine()
