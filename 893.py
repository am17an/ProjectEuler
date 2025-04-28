def calculate_t(limit):
    """
    Calculate T(N) = sum of M(n) for n from 1 to N.
    
    This version includes optimizations for large N and explores a wider variety
    of expressions to ensure we find the optimal representation for each number.
    """
    # Matchstick counts for digits and operations
    matchsticks = {
        '0': 6, '1': 2, '2': 5, '3': 5, '4': 4,
        '5': 5, '6': 6, '7': 3, '8': 7, '9': 6,
        '+': 2, '*': 2
    }

    # Function to count matchsticks for a number represented as digits
    def count_digit_matchsticks(n):
        return sum(matchsticks[d] for d in str(n))

    # Initialize memoization array for M(n)
    M = [float('inf')] * (limit + 1)
    
    # Base cases
    M[1] = matchsticks['1']  # Digit 1 requires 2 matchsticks
    
    # Calculate M(n) for each number
    for n in range(2, limit + 1):
        # Start with digit representation
        M[n] = count_digit_matchsticks(n)
        
        # Try factorizations (multiplication)
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                j = n // i
                cost = M[i] + matchsticks['*'] + M[j]
                M[n] = min(M[n], cost)
        
        # Try additions
        for i in range(1, n):
            cost = M[i] + matchsticks['+'] + M[n-i]
            M[n] = min(M[n], cost)
        
        # For small numbers, also try more complex expressions
        if n <= 10000:  # Limit for computational efficiency
            # Try expressions of form a*b+c where a,b,c are optimally represented
            for a in range(2, min(100, n)):
                for b in range(2, min(100, n)):
                    if a * b < n:
                        c = n - a * b
                        cost = M[a] + matchsticks['*'] + M[b] + matchsticks['+'] + M[c]
                        M[n] = min(M[n], cost)
        
        # Special check for numbers that might be efficiently represented as a product of powers
        # Check if n can be represented as a product of low-matchstick digits repeated
        # For example, powers of 7, 4, or 1, or products like 7*7*7
        
        # Check powers and products of 7 (which uses only 3 matchsticks)
        temp = n
        power_of_7 = True
        while temp > 1 and power_of_7:
            if temp % 7 == 0:
                temp //= 7
            else:
                power_of_7 = False
        
        if power_of_7 and temp == 1:
            # This number is 7^k for some k
            # Calculate cost: k instances of 7 and k-1 multiplication symbols
            k = 0
            temp = n
            while temp > 1:
                temp //= 7
                k += 1
            
            cost = k * matchsticks['7'] + (k - 1) * matchsticks['*']
            M[n] = min(M[n], cost)
        
        # Similarly check for powers of 4 and other efficient representations
        temp = n
        power_of_4 = True
        while temp > 1 and power_of_4:
            if temp % 4 == 0:
                temp //= 4
            else:
                power_of_4 = False
        
        if power_of_4 and temp == 1:
            # This number is 4^k for some k
            k = 0
            temp = n
            while temp > 1:
                temp //= 4
                k += 1
            
            cost = k * matchsticks['4'] + (k - 1) * matchsticks['*']
            M[n] = min(M[n], cost)
        
        # Print progress periodically
        if n % 100000 == 0:
            print(f"Calculated up to M({n}) = {M[n]}")
    
    # Calculate T(N) = sum of M(n) for n from 1 to N
    total = sum(M[1:limit+1])
    
    return total

# First verify T(100)
t_100 = calculate_t(100)
print(f"T(100) = {t_100}")

# Now calculate T(10^6) - this will take significant time
print("Starting calculation for T(10^6)...")
t_million = calculate_t(1000000)
print(f"T(10^6) = {t_million}")