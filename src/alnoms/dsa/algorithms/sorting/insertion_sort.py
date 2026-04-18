"""
Insertion Sort.

Implements the classic insertion sort algorithm, which builds the sorted
array incrementally by inserting each element into its correct position
relative to the already‑sorted prefix. The algorithm performs extremely
well on partially sorted arrays and small subarrays. An optional
visualization mode yields intermediate array states after each swap.

Design Characteristics:
- In‑place sorting
- Stable behavior
- O(N) best‑case time on nearly sorted input
- O(N²) worst‑case time
- O(1) auxiliary space
- Visualization mode yields swap‑step snapshots

Classes:
    InsertionSort: Static implementation of insertion sort.
"""

from typing import List, Generator, Union, Any


class InsertionSort:
    """Insertion sort implementation.

    Builds the sorted array one element at a time by shifting larger
    elements to the right and inserting the current element into its
    correct position. Particularly effective for small or partially
    sorted datasets.
    """

    @staticmethod
    def insertion_sort(
        arr: List[Any], visualize: bool = False
    ) -> Union[List[Any], Generator[List[Any], None, None]]:
        """Sorts the input list using insertion sort.

        If ``visualize`` is True, the function returns a generator that
        yields the array state after each swap. Otherwise, it returns the
        fully sorted list.

        Args:
            arr (List[Any]): The list to sort.
            visualize (bool): Whether to yield intermediate states.

        Returns:
            Union[List[Any], Generator[List[Any], None, None]]:
                Sorted list or generator of intermediate states.

        Complexity:
            Time: O(N²) worst case, O(N) best case
            Space: O(1)
        """
        data = list(arr)
        n = len(data)

        def _algo():
            for i in range(1, n):
                for j in range(i, 0, -1):
                    if data[j] < data[j - 1]:
                        data[j], data[j - 1] = data[j - 1], data[j]
                        if visualize:
                            yield list(data)
                    else:
                        break
            if not visualize:
                yield list(data)

        gen = _algo()
        return gen if visualize else list(gen)[-1]
