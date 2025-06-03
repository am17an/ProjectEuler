def matrix_multiply(A, B, mod):
    """Multiply two matrices A and B modulo mod"""
    n = len(A)
    m = len(B[0])
    p = len(B)
    
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % mod
    return result

def matrix_power(matrix, power, mod):
    """Compute matrix^power modulo mod using fast exponentiation"""
    n = len(matrix)
    # Initialize result as identity matrix
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    
    base = [row[:] for row in matrix]  # Copy matrix
    
    while power > 0:
        if power % 2 == 1:
            result = matrix_multiply(result, base, mod)
        base = matrix_multiply(base, base, mod)
        power //= 2
    
    return result

def print_matrix(matrix, title="Matrix"):
    """Helper function to print a matrix nicely"""
    print(f"\n{title}:")
    for row in matrix:
        print([f"{x:2d}" for x in row])

def count_simple_matrix(target_length, alphabet_size=7, mod=10**9):
    """
    Use matrix exponentiation to compute f(target_length) mod 10^9
    
    State vector: [dp[i][1], dp[i][2], dp[i][3], dp[i][4], dp[i][5], dp[i][6]]
    
    The transition matrix T is 6x6 where T[i][j] represents the coefficient
    for transitioning from state j+1 to state i+1.
    
    Transitions:
    - dp[i][j+1] += dp[i-1][j] * (alphabet_size - j) for j < alphabet_size-1
    - dp[i][1] += dp[i-1][j] * j for all j
    
    Matrix structure:
    T[0][j] = j+1 (transition to state 1 by repeating a character)
    T[j+1][j] = alphabet_size - (j+1) (transition to next state by adding new char)
    """
    if target_length == 1:
        return alphabet_size % mod
    
    # Create transition matrix
    # States: dp[i][1], dp[i][2], dp[i][3], dp[i][4], dp[i][5], dp[i][6]
    # Matrix size: 6x6 (since we track unique characters from 1 to 6)
    n = alphabet_size - 1  # 6 states
    transition = [[0] * n for _ in range(n)]
    
    for used in range(1, alphabet_size):  # used = 1 to 6
        state_idx = used - 1  # 0-indexed
        
        # Transition 1: Add new character (if possible)
        if used < alphabet_size - 1:  # used < 6
            next_state_idx = used  # used+1 - 1
            remaining = alphabet_size - used
            transition[next_state_idx][state_idx] = remaining
        
        # Transition 2: Repeat any character -> reset to 1 unique
        reset_state_idx = 0  # state 1 -> index 0
        transition[reset_state_idx][state_idx] = (transition[reset_state_idx][state_idx] + used) % mod
    
    # Initial state vector for length 1: [7, 0, 0, 0, 0, 0]
    initial_state = [alphabet_size] + [0] * (n - 1)
    
    # Compute transition^(target_length-1)
    result_matrix = matrix_power(transition, target_length - 1, mod)
    
    # Apply to initial state
    final_state = [0] * n
    for i in range(n):
        for j in range(n):
            final_state[i] = (final_state[i] + result_matrix[i][j] * initial_state[j]) % mod
    
    # Sum all states
    return sum(final_state) % mod

def count_simple_original(target_length, alphabet_size=7):
    """Original DP solution for verification"""
    # dp[length][unique_used] = number of ways
    dp = [[0 for _ in range(alphabet_size + 1)] for _ in range(target_length + 1)]
    
    # Base case: first character
    dp[1][1] = alphabet_size  # can choose any of the 7 characters
    
    for i in range(2, target_length + 1):
        for used in range(1, alphabet_size):
            if dp[i-1][used] == 0:
                continue
                
            # Transition 1: Add new character
            if used < alphabet_size - 1:
                remaining = alphabet_size - used
                dp[i][used + 1] += dp[i-1][used] * remaining
            
            # Transition 2: Repeat any character -> reset to 1 unique
            dp[i][1] += dp[i-1][used] * used
    
    print(dp[target_length])
    return sum(dp[target_length])

# Test with small values first
print("Testing with small values:")
for n in [1, 2, 3, 4, 5, 7, 8]:
    original = count_simple_original(n)
    matrix_result = count_simple_matrix(n)
    print(f"n={n}: Original={original}, Matrix={matrix_result}, Match={original == matrix_result}")

# Show the transition matrix structure
print("\nTransition Matrix Structure:")
n = 6  # 6 states for alphabet_size=7
transition = [[0] * n for _ in range(n)]
for used in range(1, 7):  # used = 1 to 6
    state_idx = used - 1  # 0-indexed
    
    # Transition 1: Add new character (if possible)
    if used < 6:  # used < 6
        next_state_idx = used  # used+1 - 1
        remaining = 7 - used
        transition[next_state_idx][state_idx] = remaining
    
    # Transition 2: Repeat any character -> reset to 1 unique
    reset_state_idx = 0  # state 1 -> index 0
    transition[reset_state_idx][state_idx] = transition[reset_state_idx][state_idx] + used

print_matrix(transition, "6x6 Transition Matrix (states 1-6)")
print("Row i, Col j: coefficient for dp[t][i+1] += dp[t-1][j+1] * coefficient")

print("\nComputing f(10^12) mod 10^9:")
result = count_simple_matrix(10**12, mod=10**9)
print(f"f(10^12) mod 10^9 = {result}")