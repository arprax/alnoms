"""
Quick Sort (3‑Way Partitioning).

Implements Dijkstra’s 3‑way partitioning variant of Quicksort, which
handles duplicate keys efficiently by dividing the array into three
regions: less than, equal to, and greater than the pivot. This approach
improves performance on inputs with many repeated values.

Design Characteristics:
- In‑place sorting
- Average‑case O(N log N) time
- Worst‑case O(N²) time (rare with randomized input)
- O(log N) recursion depth
- Optional visualization mode yielding intermediate array states

Classes:
    QuickSort: Static implementation of 3‑way partitioning Quicksort.
"""

from typing import List, Generator, Union, Any


class QuickSort:
    """3‑way partitioning Quicksort implementation.

    Uses Dijkstra’s partitioning strategy to efficiently handle arrays
    with many duplicate keys. The algorithm recursively sorts the
    subarrays containing elements less than and greater than the pivot.
    """

    @staticmethod
    def quick_sort(
        arr: List[Any], visualize: bool = False
    ) -> Union[List[Any], Generator[List[Any], None, None]]:
        """Sorts the input list using 3‑way partitioning Quicksort.

        If ``visualize`` is True, the function returns a generator that
        yields the array state after each swap or partitioning step.
        Otherwise, it returns the fully sorted list.

        Args:
            arr (List[Any]): The list to sort.
            visualize (bool): Whether to yield intermediate states.

        Returns:
            Union[List[Any], Generator[List[Any], None, None]]:
                Sorted list or generator of intermediate states.

        Complexity:
            Time: O(N log N) average, O(N²) worst‑case
            Space: O(log N) recursion
        """
        data = list(arr)

        def _sort(lo: int, hi: int):
            if hi <= lo:
                return

            lt, i, gt = lo, lo + 1, hi
            pivot = data[lo]

            while i <= gt:
                if data[i] < pivot:
                    data[lt], data[i] = data[i], data[lt]
                    lt += 1
                    i += 1
                    if visualize:
                        yield list(data)
                elif data[i] > pivot:
                    data[i], data[gt] = data[gt], data[i]
                    gt -= 1
                    if visualize:
                        yield list(data)
                else:
                    i += 1

            yield from _sort(lo, lt - 1)
            yield from _sort(gt + 1, hi)

        def _wrapper():
            yield from _sort(0, len(data) - 1)
            if not visualize:
                yield data

        gen = _wrapper()
        return gen if visualize else list(gen)[-1]
