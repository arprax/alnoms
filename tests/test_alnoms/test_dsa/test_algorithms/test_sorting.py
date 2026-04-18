from alnoms.dsa.algorithms.sorting.bubble_sort import BubbleSort
from alnoms.dsa.algorithms.sorting.insertion_sort import InsertionSort
from alnoms.dsa.algorithms.sorting.merge_sort import MergeSort
from alnoms.dsa.algorithms.sorting.quick_sort import QuickSort
from alnoms.dsa.algorithms.sorting.selection_sort import SelectionSort


def _sorted_result(sort_fn):
    arr = [3, 1, 2]
    return sort_fn(arr, visualize=False)


def test_bubble_sort_sorts():
    assert _sorted_result(BubbleSort.bubble_sort) == [1, 2, 3]


def test_insertion_sort_sorts():
    assert _sorted_result(InsertionSort.insertion_sort) == [1, 2, 3]


def test_merge_sort_sorts():
    assert _sorted_result(MergeSort.merge_sort) == [1, 2, 3]


def test_quick_sort_sorts():
    assert _sorted_result(QuickSort.quick_sort) == [1, 2, 3]


def test_selection_sort_sorts():
    assert _sorted_result(SelectionSort.selection_sort) == [1, 2, 3]
