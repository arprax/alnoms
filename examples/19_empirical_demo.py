# Purpose: Depth-3 nested loop -> cubic override
def cubic_matrix(n):
    # We must accept 'n' as the scaling factor
    A = [[1 for _ in range(n)] for _ in range(n)]
    B = [[1 for _ in range(n)] for _ in range(n)]
    C = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


# 🛰️ THE DATA GENERATOR CONTRACT
# The engine looks for this specific name to know how to scale 'N'
def data_gen(n):
    # Return the arguments required by your target function
    return (n,)


if __name__ == "__main__":
    # We must call the function at least once so the Profiler
    # identifies it as a "slow function" to target.
    cubic_matrix(10)
