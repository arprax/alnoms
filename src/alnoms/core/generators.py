"""
Alnoms: Data Generators.

Provides deterministic, dependency‑optional dataset generators used across
the Alnoms ecosystem for algorithm benchmarking, stress testing, empirical
scaling experiments, and reproducible research workflows. These utilities
serve as the canonical source of synthetic input data for:

    • Doubling tests and empirical complexity estimation
    • Worst‑case and best‑case scenario construction
    • Sorting, searching, and graph algorithm evaluation
    • Teaching, demonstrations, and notebook‑based exploration

All generators are side‑effect‑free and designed for OSS‑tier portability.
NumPy is used opportunistically for high‑volume workloads but is never
required.
"""

import random
from typing import List


class DataGenerator:
    """Collection of deterministic and high‑performance dataset generators.

    These generators are used throughout the Alnoms ecosystem for:

    - Algorithm benchmarking
    - Worst‑case and best‑case scenario construction
    - Empirical scaling tests (doubling tests)
    - Teaching and demonstration notebooks
    - Reproducible research workflows

    All methods are static and side‑effect‑free.
    """

    @staticmethod
    def random_array(n: int, lo: int = 0, hi: int = 1000) -> List[int]:
        """Generate an array of random integers.

        This is the default dependency‑free generator used across the OSS tier.
        It relies solely on Python's built‑in `random` module and is suitable
        for lightweight benchmarking or environments where NumPy is unavailable.

        Args:
            n (int): Number of integers to generate.
            lo (int): Lower bound of the random range (inclusive).
            hi (int): Upper bound of the random range (inclusive).

        Returns:
            List[int]: A list of `n` random integers.
        """
        return [random.randint(lo, hi) for _ in range(n)]

    @staticmethod
    def sorted_array(n: int, reverse: bool = False) -> List[int]:
        """Generate a sorted array of integers from 0 to n‑1.

        Useful for constructing best‑case or worst‑case inputs for sorting
        algorithms and search routines.

        Args:
            n (int): Number of elements to generate.
            reverse (bool): If True, return the array in descending order.

        Returns:
            List[int]: A sorted list of integers.
        """
        arr = list(range(n))
        if reverse:
            arr.reverse()
        return arr

    @staticmethod
    def reverse_sorted_array(n: int) -> List[int]:
        """Generate a descending array from n‑1 to 0.

        This is a convenience wrapper around `sorted_array(reverse=True)` and
        is frequently used to construct worst‑case inputs for algorithms such
        as insertion sort or bubble sort.

        Args:
            n (int): Number of elements to generate.

        Returns:
            List[int]: A descending list of integers.
        """
        return DataGenerator.sorted_array(n, reverse=True)

    @staticmethod
    def large_scale_dataset(n: int) -> List[int]:
        """Generate a large dataset optimized for high‑volume research.

        Attempts to use NumPy for high‑throughput integer generation. If NumPy
        is unavailable, falls back to the pure‑Python `random_array` generator.

        Args:
            n (int): Number of integers to generate.

        Returns:
            List[int]: A list of random integers suitable for large‑scale tests.
        """
        try:
            import numpy as np

            return np.random.randint(0, 1000, n).tolist()  # pragma: no cover
        except ImportError:
            return DataGenerator.random_array(n)

    @staticmethod
    def square_matrices(n: int) -> tuple:
        """Generate a pair of N×N matrices filled with constant values.

        Designed for benchmarking matrix multiplication algorithms where the
        computational complexity—not the numerical values—is the primary focus.

        Complexity:
            - Time: O(N²) to initialize both matrices.
            - Space: O(N²) for storage.

        Args:
            n (int): Dimension of each square matrix.

        Returns:
            tuple: A tuple `(matrix_a, matrix_b)` where:
                - `matrix_a` is filled with 1s
                - `matrix_b` is filled with 2s
        """
        matrix_a = [[1 for _ in range(n)] for _ in range(n)]
        matrix_b = [[2 for _ in range(n)] for _ in range(n)]
        return (matrix_a, matrix_b)

    @staticmethod
    def random_string(n: int, alphabet="abcdefghijklmnopqrstuvwxyz") -> str:
        return "".join(random.choice(alphabet) for _ in range(n))
