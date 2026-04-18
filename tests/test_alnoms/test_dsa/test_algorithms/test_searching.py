from alnoms.dsa.algorithms.searching.binary_search import BinarySearch


def test_binary_search_search_and_rank():
    arr = [1, 3, 5, 7]
    assert BinarySearch.search(arr, 5) == 2
    assert BinarySearch.search(arr, 2) == -1
    assert BinarySearch.rank(arr, 0) == 0
    assert BinarySearch.rank(arr, 4) == 2
    assert BinarySearch.rank(arr, 10) == 4
