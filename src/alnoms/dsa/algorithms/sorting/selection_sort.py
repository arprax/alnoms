"""
Selection Sort.

Provides a simple comparison‑based sorting algorithm that repeatedly
selects the minimum element and swaps it into its correct position.
This implementation supports optional step‑by‑step visualization via a
generator interface.

Design Characteristics:
- In‑place sorting
- Deterministic O(N²) time
- O(1) auxiliary space
- Visualization mode yields intermediate array states

Classes:
    SelectionSort: Static implementation of the selection sort algorithm.
"""

from typing import List, Generator, Union, Any


class SelectionSort:
    """Selection sort implementation.

    Repeatedly scans the unsorted portion of the array to find the
    minimum element and swaps it into its correct position. The algorithm
    is simple, stable in behavior, and useful for educational and
    demonstrative purposes.
    """

    @staticmethod
    def selection_sort(
        arr: List[Any], visualize: bool = False
    ) -> Union[List[Any], Generator[List[Any], None, None]]:
        """Sorts the input list using selection sort.

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
            Time: O(N²)
            Space: O(1)
        """
        data = list(arr)
        n = len(data)

        def _algo():
            for i in range(n):
                min_idx = i
                for j in range(i + 1, n):
                    if data[j] < data[min_idx]:
                        min_idx = j
                data[i], data[min_idx] = data[min_idx], data[i]
                if visualize:
                    yield list(data)
            if not visualize:
                yield list(data)

        gen = _algo()
        return gen if visualize else list(gen)[-1]
