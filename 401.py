mod = int(1e9)
def sum_k_squared_floor_n_div_k(n):
    """
    Calculate the summation of K²⌊N/K⌋ for K from 1 to N in O(sqrt(N)) time.
    
    Args:
        n: Upper limit of summation
        
    Returns:
        The sum of K²⌊N/K⌋ for K from 1 to N
    """
    total = 0
    
    # For each distinct value of ⌊N/K⌋
    i = 1
    while i <= n:
        # d is the value of ⌊N/K⌋
        d = n // i

        steps += 1

        # Find the upper bound for this value of d
        j = n // d
        
        # Sum of squares formula: Σ(i² to j²) = (j(j+1)(2j+1) - i(i-1)(2i-1))/6
        sum_squares = (j * (j + 1) * (2 * j + 1) - i * (i - 1) * (2 * i - 1)) // 6
        
        # Add the contribution of this range to the total
        total += d * sum_squares
        total %= mod
        
        # Move to the next distinct value of ⌊N/K⌋
        i = j + 1
    
    return total


def sum_k_squared_floor_n_div_k_brute_force(n):
    """
    Calculate the summation using brute force O(N) approach for verification.
    """
    total = 0
    for k in range(1, n + 1):
        total += k * k * (n // k)
    return total


# Test cases
if __name__ == "__main__":
    test_cases = [6, 100, 1000, 10000, int(1e15)]
    
    for n in test_cases:
        efficient_result = sum_k_squared_floor_n_div_k(n)
        
        # For small values, verify with brute force
        if n <= 1000:
            brute_force_result = sum_k_squared_floor_n_div_k_brute_force(n)
            print(f"N = {n}, Efficient: {efficient_result}, Brute Force: {brute_force_result}")
            assert efficient_result == brute_force_result
        else:
            print(f"N = {n}, Result: {efficient_result}")