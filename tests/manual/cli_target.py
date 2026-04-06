"""
Manual Test Target for the Alnoms CLI.
Run via: alnoms analyze tests/manual/cli_target.py
"""


# The data generator required by the Alnoms standard for Empirical Math
def data_gen(n):
    return list(range(n))


# A terribly inefficient O(N^2) function to trigger the governance failure
def process_data(arr):
    result = []
    for i in arr:
        for j in arr:
            if i == j:
                result.append(i)
    return result


if __name__ == "__main__":
    # Local execution block just in case it's run directly
    data = data_gen(500)
    process_data(data)
