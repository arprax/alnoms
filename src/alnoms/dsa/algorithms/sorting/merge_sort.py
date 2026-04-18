"""
Merge Sort.

Implements the classic divide‑and‑conquer merge sort algorithm using an
auxiliary array for merging. The algorithm guarantees O(N log N) time
regardless of input distribution and is stable by construction. An
optional visualization mode yields intermediate array states after each
merge operation.

Design Characteristics:
- Stable sorting
- Deterministic O(N log N) time
- Requires O(N) auxiliary space
- Visualization mode yields merge‑step snapshots

Classes:
    MergeSort: Static implementation of top‑down merge sort.
"""

from typing import List, Generator, Union, Any


class MergeSort:
    """Top‑down recursive merge sort implementation.

    The algorithm recursively divides the array into halves, sorts each
    half, and merges them using an auxiliary array. This version supports
    visualization by yielding intermediate states after each merge step.
    """

    @staticmethod
    def merge_sort(
        arr: List[Any], visualize: bool = False
    ) -> Union[List[Any], Generator[List[Any], None, None]]:
        """Sorts the input list using merge sort.

        If ``visualize`` is True, the function returns a generator that
        yields the array state after each merge operation. Otherwise, it
        returns the fully sorted list.

        Args:
            arr (List[Any]): The list to sort.
            visualize (bool): Whether to yield intermediate states.

        Returns:
            Union[List[Any], Generator[List[Any], None, None]]:
                Sorted list or generator of intermediate states.

        Complexity:
            Time: O(N log N)
            Space: O(N) auxiliary array
        """
        data = list(arr)
        aux = list(arr)

        def _merge(lo: int, mid: int, hi: int):
            # Copy to auxiliary array
            for k in range(lo, hi + 1):
                aux[k] = data[k]

            i, j = lo, mid + 1

            for k in range(lo, hi + 1):
                if i > mid:
                    data[k] = aux[j]
                    j += 1
                elif j > hi:
                    data[k] = aux[i]
                    i += 1
                elif aux[j] < aux[i]:
                    data[k] = aux[j]
                    j += 1
                else:
                    data[k] = aux[i]
                    i += 1

                if visualize:
                    yield list(data)

        def _sort(lo: int, hi: int):
            if hi <= lo:
                return
            mid = lo + (hi - lo) // 2
            yield from _sort(lo, mid)
            yield from _sort(mid + 1, hi)
            yield from _merge(lo, mid, hi)

        def _wrapper():
            yield from _sort(0, len(data) - 1)
            if not visualize:
                yield data

        gen = _wrapper()
        return gen if visualize else list(gen)[-1]
