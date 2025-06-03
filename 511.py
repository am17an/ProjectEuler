n = 1234567898765
k = 4321
import numpy as np
import cupy as cp

#n = 4
#k = 3
#n = 1111
#k = 24

digits = []

for i in range(1, int(n**0.5 + 1)):
    if n%i == 0:
        digits.append(i)
        if i != n//i:
            digits.append(n//i)


print(digits)


matrix = [[0 for i in range(k)] for j in range(k)]

for i in range(k):
    for dig in digits:
        new_mod = (i + dig)%k
        matrix[new_mod][i] = 1


initial_matrix = cp.zeros((k, 1), dtype=cp.int64)
initial_matrix[n%k,:] = 1


MOD = 10**9 + 7  # Standard modulus for Project Euler problems
C = matrix

def matrix_power(M, exponent, mod):
    if exponent == 0:
        return np.identity(M.shape[0], dtype=np.int64) % mod
    if exponent == 1:
        return M % mod

    half = matrix_power(M, exponent // 2, mod)
    result = np.matmul(half, half) % mod

    if exponent % 2 == 0:
        return result
    else:
        return np.matmul(M, result) % mod


def modular_matmul(A, B, mod):
    """Perform matrix multiplication with modular arithmetic"""
    # Simple approach: since we're applying mod at each step of exponentiation,
    # the values shouldn't grow too large
    result = cp.matmul(A, B) % mod
    return result

def matrix_power_gpu(M, exponent, mod):
    if exponent == 0:
        return cp.identity(M.shape[0], dtype=cp.int64) % mod
    if exponent == 1:
        return M % mod

    half = matrix_power_gpu(M, exponent // 2, mod) % mod
    # Use modular matrix multiplication to prevent overflow
    result = modular_matmul(half, half, mod)

    if exponent % 2 == 0:
        return result
    else:
        # Apply modular arithmetic to prevent overflow
        return modular_matmul(M % mod, result, mod)

C = cp.array(C, dtype=cp.int64)
matrix = matrix_power_gpu(C, n, MOD)


print(initial_matrix)
result = modular_matmul(matrix, initial_matrix, MOD)

print(result)


"""
#dp = [[0 for i in range(k)] for j in range(n+1)]

dp[0][n%k] = 1

for n in range(1, n+1):
    for mod in range(0, k):
        for d in digits:
            new_mod = (mod + d)%k
            dp[n][new_mod] += dp[n-1][mod]
"""

#print(dp[n][0])
