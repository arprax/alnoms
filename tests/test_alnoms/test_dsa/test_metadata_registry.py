from alnoms.dsa.metadata import MetadataRegistry


def test_get_metadata_known_and_unknown():
    # Known algorithm (snake_case)
    m = MetadataRegistry.get_metadata("merge_sort")
    assert m["complexity"].startswith("O(")

    # Unknown algorithm → fallback entry
    unknown = MetadataRegistry.get_metadata("nonexistent_algo")
    assert unknown["complexity"] == "Unknown"
    assert unknown["tier"] == "OSS"
    assert unknown["module"] is None


def test_list_available_algorithms_by_tier():
    # OSS tier should include merge_sort
    oss = MetadataRegistry.list_available_algorithms("OSS")
    assert "merge_sort" in oss

    # ALL should include all snake_case keys
    all_algos = MetadataRegistry.list_available_algorithms("ALL")
    assert "merge_sort" in all_algos
    assert "quick_sort" in all_algos
    assert "binary_search" in all_algos
    assert "has_cycle" in all_algos  # CycleDetector equivalent


def test_get_all_contains_core_entries():
    all_meta = MetadataRegistry.get_all()

    # Sorting
    assert "merge_sort" in all_meta
    assert "quick_sort" in all_meta

    # Structures
    assert "separate_chaining_hash" in all_meta
    assert "stack" in all_meta
    assert "queue" in all_meta

    # Graph algorithms
    assert "bfs_paths" in all_meta
    assert "dijkstra" in all_meta
