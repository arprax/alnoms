from alnoms.dsa.structures import SeparateChainingHashST


def fast_membership_sum(arr):
    # Convert list to an optimized hash structure
    st = SeparateChainingHashST()
    for item in arr:
        st.put(item, item)

    total = 0
    for x in arr:
        # O(1) lookup vs original O(N)
        if st.contains(x):
            total += x
    return total


# Required for empirical scaling
def data_gen(n):
    return (list(range(n)),)


if __name__ == "__main__":
    data = list(range(200))
    print(fast_membership_sum(data))
