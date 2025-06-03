# Helper function for modular exponentiation
def power(base, exp, mod):
    res = 1
    base %= mod # Ensures base is within [0, mod-1] or handles negative base
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp //= 2
    return res

# Helper function for modular inverse (using Fermat's Little Theorem as mod is prime)
def modInverse(n, mod):
    return power(n, mod - 2, mod)

# Helper function for 2x2 matrix multiplication modulo mod
def matrix_mult(A, B, mod):
    C = [[0, 0], [0, 0]]
    C[0][0] = (A[0][0] * B[0][0] + A[0][1] * B[1][0]) % mod
    C[0][1] = (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % mod
    C[1][0] = (A[1][0] * B[0][0] + A[1][1] * B[1][0]) % mod
    C[1][1] = (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % mod
    return C

# Helper function for 2x2 matrix exponentiation modulo mod
def matrix_pow(matrix, exp, mod):
    res_matrix = [[1, 0], [0, 1]] # Identity matrix
    base_matrix = matrix
    while exp > 0:
        if exp % 2 == 1:
            res_matrix = matrix_mult(res_matrix, base_matrix, mod)
        base_matrix = matrix_mult(base_matrix, base_matrix, mod)
        exp //= 2
    return res_matrix

def solve():
    N_val = 10**18
    MOD = 1000000009

    # Standard Fibonacci matrix M_F = [[F_2, F_1], [F_1, F_0]] = [[1,1],[1,0]]
    # M_F^k = [[F_{k+1}, F_k], [F_k, F_{k-1}]]
    M_F = [[1, 1], [1, 0]]

    # We need F_{N-1} and F_N.
    # Calculate M_F^(N-1).
    # If N_val = 1, then N_val - 1 = 0. matrix_pow(M_F, 0, MOD) gives identity [[1,0],[0,1]].
    # Then F_0 = (Identity)_{0,1} = 0, and F_1 = (Identity)_{0,0} = 1. Correct.
    
    # exp_for_fib = N_val - 1. If N_val is 0, this is -1.
    # Problem context implies N >= 1. Smallest N could be 1.
    if N_val == 0:
        # This case is not expected for this problem, F_{-1} would be needed.
        # The formula implies N >= 1.
        # For N=0, F_{N-1} = F_{-1}. Standard F_{-1}=1.
        # L_0 = 2.
        # (-2)^0 = 1, (-4)^0 = 1.
        # Num = 1*1 - 1 = 0. Denom = 1 - 1*2 + 1 = 0.  P(0) is 0/0, problematic.
        # Let's assume N_val >= 1 from problem context.
        print("N=0 is not handled by this setup based on F_{N-1}.")
        return

    mat_N_minus_1 = matrix_pow(M_F, N_val - 1, MOD)

    f_N_minus_1 = mat_N_minus_1[0][1] # This corresponds to F_k if exponent is k. Here, F_{N-1}.
    f_N = mat_N_minus_1[0][0]         # This corresponds to F_{k+1} if exponent is k. Here, F_N.

    # Calculate L_N = 2*F_{N-1} + F_N (mod MOD)
    l_N = (2 * f_N_minus_1 + f_N) % MOD
    # Ensure l_N is positive if intermediate was negative, though Python's % should handle it.
    if l_N < 0: l_N += MOD


    # Calculate (-2)^N and (-4)^N modulo MOD
    # Python's pow(base, exp, mod) handles negative base correctly by (base % mod + mod) % mod effectively
    term_neg_2_pow_N = power(-2, N_val, MOD)
    term_neg_4_pow_N = power(-4, N_val, MOD)

    # Numerator: (-2)^N * F_{N-1} - 1 (mod MOD)
    num_val_term1 = (term_neg_2_pow_N * f_N_minus_1) % MOD
    num_val = (num_val_term1 - 1 + MOD) % MOD # Add MOD before final % to handle potential negative result

    # Denominator: (-4)^N - (-2)^N * L_N + 1 (mod MOD)
    den_val_term_mult = (term_neg_2_pow_N * l_N) % MOD
    den_val_intermediate = (term_neg_4_pow_N - den_val_term_mult + MOD) % MOD
    den_val = (den_val_intermediate + 1 + MOD) % MOD

    if den_val == 0:
        # This should not happen for a well-posed Project Euler problem
        # where P(N) is a defined rational number and Q is sought.
        # If it does, means P(N)'s denominator is a multiple of MOD.
        # If num_val is also 0, Q could be 1. If num_val non-zero, Q is undefined.
        print("Error: Denominator is zero modulo MOD. Problem might be ill-defined for this MOD.")
        return

    # P(N) = num_val / den_val (mod MOD)
    # q such that num_val = den_val * q (mod MOD)
    # q = num_val * modInverse(den_val, MOD) (mod MOD)
    den_inv = modInverse(den_val, MOD)
    prob_val_q = (num_val * den_inv) % MOD

    # Q is the smallest *positive* q.
    # If prob_val_q is 0, it means num_val was 0 (assuming den_val non-zero).
    # Then 0 = den_val * q (mod MOD). Smallest positive q is MOD.
    result_q = prob_val_q
    if result_q == 0:
        result_q = MOD
        
    print(result_q)

if __name__ == '__main__':
    solve()
