from alnoms.dsa.metadata import MetadataRegistry
from alnoms.core.decision_engine import DecisionEngine


def test_decide_algorithm_basic_rules():
    engine = DecisionEngine(MetadataRegistry.get_all())

    assert engine.decide("inefficient_membership") == "separate_chaining_hash_st"
    assert engine.decide("redundant_sort") == "merge_sort"
    assert engine.decide("inplace_concat") == "list_concat"


def test_decide_algorithm_nested_loops():
    engine = DecisionEngine(MetadataRegistry.get_all())

    assert engine.decide("nested_loops", "membership") == "separate_chaining_hash_st"
    assert engine.decide("nested_loops", "sorting") == "merge_sort"
    assert engine.decide("nested_loops", "dfs") == "graph_traversal"
    assert engine.decide("nested_loops", "generic") == "pruning"


def test_decide_metadata():
    engine = DecisionEngine(MetadataRegistry.get_all())

    # Should normalize PascalCase → snake_case
    meta = engine.decide_metadata("MergeSort")
    assert meta["category"] == "sorting"
    assert meta["complexity"].startswith("O(")

    # Direct snake_case lookup
    meta2 = engine.decide_metadata("merge_sort")
    assert meta2["category"] == "sorting"
