# Purpose: Sorting inside loop → merge_sort cure
def redundant_sort(arrays):
    result = []
    for arr in arrays:
        arr.sort()
        result.append(arr[0])
    return result
