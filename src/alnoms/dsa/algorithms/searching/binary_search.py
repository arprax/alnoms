"""
Binary Search Utilities.

Provides classic binary search operations on sorted arrays, including
exact‑match search and rank computation. Both operations run in O(log N)
time and assume that the input list is already sorted in ascending
order.

Design Characteristics:
- Deterministic O(log N) time
- Works on any comparable key type
- Rank operation supports arrays with duplicates
- No side effects; functions operate on the input list as read‑only

Classes:
    BinarySearch: Static utilities for binary search and rank.
"""

from typing import List, Any


class BinarySearch:
    """Binary search and rank utilities.

    Implements exact‑match binary search and a left‑leaning rank
    operation that counts how many elements are strictly less than a
    given key. Both methods assume the input list is sorted.
    """

    @staticmethod
    def search(a: List[Any], key: Any) -> int:
        """Performs binary search for ``key`` in a sorted list.

        Args:
            a (List[Any]): Sorted list to search.
            key (Any): Target key.

        Returns:
            int: Index of ``key`` if found, otherwise -1.

        Complexity:
            Time: O(log N)
            Space: O(1)
        """
        lo = 0
        hi = len(a) - 1

        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if key < a[mid]:
                hi = mid - 1
            elif key > a[mid]:
                lo = mid + 1
            else:
                return mid
        return -1

    @staticmethod
    def rank(a: List[Any], key: Any) -> int:
        """Returns the number of elements strictly less than ``key``.

        Uses a left‑leaning binary search to find the first index at
        which ``key`` could be inserted while maintaining sorted order.
        This yields the count of elements smaller than ``key`` and works
        efficiently even with many duplicates.

        Args:
            a (List[Any]): Sorted list to examine.
            key (Any): Target key.

        Returns:
            int: Count of elements strictly less than ``key``.

        Complexity:
            Time: O(log N)
            Space: O(1)
        """
        lo = 0
        hi = len(a) - 1

        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if key <= a[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        return lo
