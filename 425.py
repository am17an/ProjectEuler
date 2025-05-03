from collections import deque

def sieve_of_eratosthenes(n):
    """Generate all primes up to n using the Sieve of Eratosthenes."""
    if n < 2:
        return [], []
    
    # Initialize boolean array with True values
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    # Main sieve logic
    p = 2
    while p * p <= n:
        if is_prime[p]:
            # Mark all multiples of p as non-prime
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    
    # Collect prime numbers
    primes = [i for i in range(2, n + 1) if is_prime[i]]
    return primes, is_prime

def find_2s_relatives(n):
    """
    Find all primes up to n that are 2's relatives.
    A prime P is a 2's relative if there exists a chain of connected primes 
    between 2 and P, and no prime in the chain exceeds P.
    """
    _, is_prime = sieve_of_eratosthenes(n)
    
    # Dictionary to store the minimum maximum prime in any path from 2 to each prime
    min_max_prime = {2: 2}  # For prime 2, the max prime in the path is 2 itself
    
    # Queue for BFS, starting from prime 2
    queue = deque([2])
    
    while queue:
        current = queue.popleft()
        current_max = min_max_prime[current]
        
        # Find all connected primes
        connected_primes = []
        str_current = str(current)
        
        # Rule 1: Same length, differ in exactly one digit
        for i in range(len(str_current)):
            for d in range(10):
                if i == 0 and d == 0:  # Skip leading zeros
                    continue
                
                new_digits = list(str_current)
                new_digits[i] = str(d)
                new_prime = int(''.join(new_digits))
                
                if new_prime != current and new_prime <= n and is_prime[new_prime]:
                    connected_primes.append(new_prime)
        
        # Rule 2a: Remove leftmost digit
        if len(str_current) > 1:
            new_prime = int(str_current[1:])
            if new_prime > 1 and is_prime[new_prime]:
                connected_primes.append(new_prime)
        
        # Rule 2b: Add digit to the left
        for d in range(1, 10):  # Start from 1 to avoid leading zeros
            new_prime = int(str(d) + str_current)
            if new_prime <= n and is_prime[new_prime]:
                connected_primes.append(new_prime)
        
        # Process connected primes
        for connected in connected_primes:
            # Calculate the new maximum prime in the path
            new_max = max(current_max, connected)
            
            # If we haven't seen this prime before, or if this path has a smaller maximum
            if connected not in min_max_prime or new_max < min_max_prime[connected]:
                min_max_prime[connected] = new_max
                queue.append(connected)
    
    # A prime P is a 2's relative if the maximum prime in any path from 2 to P is P itself
    return min_max_prime

def calculate_F(n):
    """
    Calculate F(n), the sum of primes ≤ n that are not 2's relatives.
    """
    primes, _ = sieve_of_eratosthenes(n)
    min_max_prime = find_2s_relatives(n)
    
    # Sum of primes that are not 2's relatives
    total = 0
    for p in primes:
        # A prime is a 2's relative if it's in min_max_prime and min_max_prime[p] <= p
        if p not in min_max_prime or min_max_prime[p] > p:
            total += p
    
    return total

# Test cases
print(f"F(10^3) = {calculate_F(10**3)}")
print(f"F(10^4) = {calculate_F(10**4)}")

# Final calculation
print(f"F(10^7) = {calculate_F(10**7)}")
