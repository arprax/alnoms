from alnoms.core.generators import DataGenerator


def test_random_array_length_and_range():
    arr = DataGenerator.random_array(10, lo=0, hi=5)
    assert len(arr) == 10
    assert all(0 <= x <= 5 for x in arr)


def test_sorted_array_forward_and_reverse():
    arr = DataGenerator.sorted_array(5)
    assert arr == [0, 1, 2, 3, 4]
    arr_rev = DataGenerator.sorted_array(5, reverse=True)
    assert arr_rev == [4, 3, 2, 1, 0]


def test_square_matrices_shape():
    a, b = DataGenerator.square_matrices(3)
    assert len(a) == 3 and len(a[0]) == 3
    assert len(b) == 3 and len(b[0]) == 3
    assert all(v == 1 for row in a for v in row)
    assert all(v == 2 for row in b for v in row)
