from alnoms.fixes import get_registered_fixers, get_fixer


def test_registry_contains_all_fixers():
    ids = {f.pattern_id for f in get_registered_fixers()}
    assert ids == {
        "nested_loops",
        "redundant_sort",
        "expensive_calls",
        "high_freq_io",
        "inplace_concat",
        "inefficient_membership",
    }


def test_get_fixer_returns_correct_instance():
    assert get_fixer("nested_loops").pattern_id == "nested_loops"
    assert get_fixer("redundant_sort").pattern_id == "redundant_sort"
    assert get_fixer("expensive_calls").pattern_id == "expensive_calls"
    assert get_fixer("high_freq_io").pattern_id == "high_freq_io"
    assert get_fixer("inplace_concat").pattern_id == "inplace_concat"
    assert get_fixer("inefficient_membership").pattern_id == "inefficient_membership"
    assert get_fixer("unknown") is None
