import numpy as np

def calculate_expected_value(N, trials):
    """
    Calculate the expected value for a given N and number of trials.
    
    For each a in {1, 2, ..., N}:
    - p = 2a(N-a+1)/N² - 1/N²
    - P(even successes) = [1 + (1-2p)^trials] / 2
    
    Returns the sum of all P(even successes)
    """
    # Using symmetry: p(a) = p(N-a+1)
    half_N = N // 2
    
    # Process in chunks to avoid memory issues but without special handling
    chunk_size = 10**6
    expected_value = 0
    
    # Process first half in chunks
    for chunk_start in range(1, half_N + 1, chunk_size):
        chunk_end = min(chunk_start + chunk_size - 1, half_N)
        
        # Create array of a values for this chunk
        a_values = np.arange(chunk_start, chunk_end + 1, dtype=np.float64)
        
        # Calculate p for each a
        p = (2 * a_values * (N - a_values + 1) - 1) / (N * N)
        
        # Calculate (1-2p)^trials using log for numerical stability
        x = 1 - 2 * p
        
        # Use log method for all power calculations
        log_term = trials * np.log(np.abs(x))
        signs = np.where(x >= 0, 1, (-1)**trials)
        powered = signs * np.exp(log_term)
        
        # Calculate P(even)
        prob_even = (1 + powered) / 2
        
        # Add to sum
        expected_value += np.sum(prob_even)
        
        if chunk_start % (10 * chunk_size) == 1:
            print(f"Processed up to {chunk_end} of {half_N}")
    
    # Double the sum due to symmetry
    expected_value *= 2
    
    # Handle the middle term if N is odd
    if N % 2 == 1:
        middle_a = half_N + 1
        middle_p = (2 * middle_a * (N - middle_a + 1) - 1) / (N * N)
        x_middle = 1 - 2 * middle_p
        
        # Same log approach for middle term
        log_term = trials * np.log(np.abs(x_middle))
        sign = 1 if x_middle >= 0 else ((-1)**trials)
        powered_middle = sign * np.exp(log_term)
        
        middle_prob = (1 + powered_middle) / 2
        expected_value += middle_prob
    
    return expected_value

# Example usage
N = 100
trials = 10
result = calculate_expected_value(N, trials)
print(f"For N={N} with {trials} trials: {result}")

# Additional test cases for verification
N = 5
trials = 4
result = calculate_expected_value(N, trials)
print(f"For N={N} with {trials} trials: {result}")

N = 20
trials = 4
result = calculate_expected_value(N, trials)
print(f"For N={N} with {trials} trials: {result}")

# Test with large N and trials
N = int(1e10)
trials = 4000
result = calculate_expected_value(N, trials)
print(f"For N={N} with {trials} trials: {result}")