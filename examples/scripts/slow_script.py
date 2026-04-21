"""Inefficient script used for the Alnoms demonstration."""


def slow_membership_sum(arr):
    total = 0
    for x in arr:
        # Intentional O(N^2) membership trap
        if x in arr:
            total += x
    return total


# Required for empirical scaling
def data_gen(n):
    return (list(range(n)),)


if __name__ == "__main__":
    data = list(range(200))
    print(slow_membership_sum(data))
