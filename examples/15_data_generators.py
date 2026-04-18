"""
Demo 15: Data Generators

Shows how to use the industrial-grade dataset generators provided by Alnoms.
These generators are used throughout the analyzer, profiler, and stress tests.
"""

from alnoms.core.generators import DataGenerator


def demo_generators():
    print("\n=== Data Generators Demo ===\n")

    # 1. Random array
    arr = DataGenerator.random_array(10, lo=0, hi=50)
    print("1) Random Array (10 elements):")
    print(arr, "\n")

    # 2. Sorted array
    sorted_arr = DataGenerator.sorted_array(10)
    print("2) Sorted Array (ascending):")
    print(sorted_arr, "\n")

    # 3. Reverse sorted array
    rev_arr = DataGenerator.sorted_array(10, reverse=True)
    print("3) Reverse Sorted Array (descending):")
    print(rev_arr, "\n")

    # 4. Large-scale dataset (NumPy if available)
    big = DataGenerator.large_scale_dataset(20)
    print("4) Large-Scale Dataset (20 elements):")
    print(big, "\n")

    # 5. Square matrices for matrix multiplication tests
    A, B = DataGenerator.square_matrices(4)
    print("5) Square Matrices (4x4):")
    print("Matrix A:")
    for row in A:
        print(row)
    print("\nMatrix B:")
    for row in B:
        print(row)
    print()


if __name__ == "__main__":
    demo_generators()
