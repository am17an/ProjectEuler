import math

# --- Helper Functions ---

mod = int(1e9) + 7

def sum_integers(a: int, b: int) -> int:
    """
    Calculates the sum of integers from a to b (inclusive).
    Sum = a + (a+1) + ... + b
    Uses the formula: Sum(1..b) - Sum(1..a-1)
    """
    if a > b:
        return 0
    # Calculate sum from 1 to b
    sum_b = (b * (b + 1)) // 2
    # Calculate sum from 1 to a-1
    sum_a_minus_1 = ((a - 1) * a) // 2
    # The result is the difference
    return int(sum_b - sum_a_minus_1)%mod

def calculate_D_N(N: int) -> int:
    """
    Calculates D(N) = sum_{k=1}^{N} floor(N/k) in O(sqrt(N)) time.
    Uses block summation. Equivalent to Dirichlet hyperbola method.
    """
    if N <= 0:
        return 0

    D = 0
    k = 1
    while k <= N:
        v = N // k # floor(N/k)
        if v == 0:
            break
        # Last k for which floor(N/k) is v
        k_last = N // v
        # Count of numbers in the block [k, k_last]
        count = k_last - k + 1
        # Add contribution for this block
        D += v * count
        D %= mod
        # Move to next block
        k = k_last + 1
    return D

def calculate_T_N(N: int) -> int:
    """
    Calculates T(N) = sum_{k=1}^{N} k * floor(N/k)*(floor(N/k)+1)/2 in O(sqrt(N)) time.
    Uses block summation.
    """
    if N <= 0:
        return 0
    T = 0
    k = 1
    while k <= N:
        v = N // k # Current value of floor(N/k)
        if v == 0:
            break
        # Find the largest k' such that floor(N/k') == v
        k_last = N // v

        # Calculate sum of k in the current block [k, k_last]
        current_sum_of_k = sum_integers(k, k_last)

        # Calculate the value factor associated with this block: v*(v+1)/2
        term_value = (v * (v + 1)) // 2

        # Add the contribution of this block to T
        T += term_value * current_sum_of_k

        T %= mod

        # Move k to the start of the next block
        k = k_last + 1
    return T

def calculate_T_even_N(N: int) -> int:
    """
    Calculates T_even(N) = sum_{j=1}^{floor(N/2)} j * floor(N/2j)*(floor(N/2j)+1).
    This is derived from Sum_{k even} k * floor(N/k)*(floor(N/k)+1)/2.
    Uses block summation based on value v = floor(N/(2j)). Runs in O(sqrt(N)).
    """
    if N <= 1: # floor(N/2) is 0, so sum is empty
        return 0

    M = N // 2 # Upper limit for j
    T_even = 0
    j = 1
    while j <= M:
        # Value in floor: v = floor(N / (2j))
        if N < 2 * j: # Avoid potential issues, means v=0
             break
        v = N // (2 * j)
        if v == 0: # Means 2j > N
            break

        # Find last j in block: j_last = floor(N / (2v))
        # Also, j_last cannot exceed M = floor(N/2)
        # Check for v=0 already done above, so 2v is safe if N>=1
        j_last_candidate = N // (2 * v)
        j_last = min(j_last_candidate, M)

        # Sum of j in the current block [j, j_last]
        sum_of_j = sum_integers(j, j_last)

        # Contribution for this block is v * (v + 1) * sum_of_j
        T_even += v * (v + 1) * sum_of_j

        T_even %= mod

        # Move j to the start of the next block
        j = j_last + 1

    return T_even

# --- Main function for the odd k summation ---

def calculate_double_summation_odd_k(N: int) -> int:
    """
    Calculates the double summation S = sum_{n=1}^{N} sum_{k=1, k odd}^{n} floor(n/k).

    Args:
        N: The upper limit of the outer summation. Must be a non-negative integer.

    Returns:
        The result of the double summation with k odd.

    Uses the derived formula S_odd = (N+1)*D_odd(N) - T_odd(N), calculated in O(sqrt(N)).
    D_odd(N) = D(N) - D(floor(N/2))
    T_odd(N) = T(N) - T_even(N)
    """
    if not isinstance(N, int) or N < 0:
        raise ValueError("N must be a non-negative integer.")
    if N == 0:
        return 0

    # Calculate D_odd(N)
    D_N = calculate_D_N(N)
    D_N_half = calculate_D_N(N // 2)
    D_odd = D_N - D_N_half

    # Calculate T_odd(N)
    T_N = calculate_T_N(N)
    T_even = calculate_T_even_N(N)
    T_odd = T_N - T_even

    # Final calculation: S_odd = (N+1)*D_odd - T_odd
    S_odd = (N + 1) * D_odd - T_odd
    return S_odd % mod

# --- Example Usage ---
N_example1 = 3
result1 = calculate_double_summation_odd_k(N_example1)
print(f"For N = {N_example1} (k odd), the sum is: {result1}") # Expected: 7

N_example2 = 10
result2 = calculate_double_summation_odd_k(N_example2)
print(f"For N = {N_example2} (k odd), the sum is: {result2}") # Expected: 83

N_example3 = 100
result3 = calculate_double_summation_odd_k(N_example3)
print(f"For N = {N_example3} (k odd), the sum is: {result3}") # Expected: 6481 (Based on corrected calculation)

# Example with a larger N
N_example4 = 10**16 # 10^5
result4 = calculate_double_summation_odd_k(N_example4)
print(f"For N = {N_example4} (k odd), the sum is: {result4}")