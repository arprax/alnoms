"""
Bubble Sort.

Implements the classic bubble sort algorithm, which repeatedly scans the
array and swaps adjacent elements that are out of order. This version
includes the standard early‑termination optimization: if a full pass
completes with no swaps, the array is already sorted. An optional
visualization mode yields intermediate array states after each swap.

Design Characteristics:
- In‑place sorting
- Stable behavior
- O(N²) average and worst‑case time
- O(N) best‑case time on already sorted input
- O(1) auxiliary space
- Visualization mode yields swap‑step snapshots

Classes:
    BubbleSort: Static implementation of bubble sort.
"""

from typing import List, Generator, Union, Any


class BubbleSort:
    """Bubble sort implementation.

    Repeatedly compares adjacent elements and swaps them if they are in
    the wrong order. The algorithm terminates early if a full pass
    completes without any swaps, making it efficient for nearly sorted
    input.
    """

    @staticmethod
    def bubble_sort(
        arr: List[Any], visualize: bool = False
    ) -> Union[List[Any], Generator[List[Any], None, None]]:
        """Sorts the input list using bubble sort.

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
            Time: O(N²) average/worst, O(N) best case
            Space: O(1)
        """
        data = list(arr)
        n = len(data)

        def _algo():
            for i in range(n):
                swapped = False
                for j in range(0, n - i - 1):
                    if data[j] > data[j + 1]:
                        data[j], data[j + 1] = data[j + 1], data[j]
                        swapped = True
                        if visualize:
                            yield list(data)
                if not swapped:
                    break
            if not visualize:
                yield list(data)

        gen = _algo()
        return gen if visualize else list(gen)[-1]
