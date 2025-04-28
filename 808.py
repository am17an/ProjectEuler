def sieve_of_eratosthenes(limit):
    """Generate all primes up to limit using Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
                
    return [i for i in range(limit + 1) if sieve[i]]

def reverse_number(n):
    """Reverse the digits of a number."""
    return int(str(n)[::-1])

def is_palindrome(n):
    """Check if a number is a palindrome."""
    return n == reverse_number(n)

def find_reversible_prime_squares(count):
    """Find the first 'count' reversible prime squares using a hashmap approach."""
    
    # Generate primes using sieve (we'll use a high enough limit)
    limit = 100000000  # This should be enough for our purposes
    primes = sieve_of_eratosthenes(limit)
    
    # Generate all prime squares and store in a hash set for O(1) lookup
    prime_squares = {}  # Maps square value to the prime that generated it
    for p in primes:
        prime_squares[p*p] = p
    
    reversible_squares = []
    seen = set()  # To avoid duplicates
    
    # Now check each prime square
    for p in primes:
        square = p * p
        
        if square in seen:
            continue
            
        reverse_square = reverse_number(square)
        
        # Check all conditions:
        # 1. Not a palindrome
        # 2. The reverse is different (should be implied by #1)
        # 3. The reverse is also a prime square
        # 4. We haven't seen either number before
        if (not is_palindrome(square) and 
            square != reverse_square and
            reverse_square in prime_squares and
            reverse_square not in seen):
            
            reversible_squares.append(square)
            reversible_squares.append(reverse_square)
            
            seen.add(square)
            seen.add(reverse_square)
            
            # Check if we've found enough
            if len(reversible_squares) >= count:
                break
    
    # Sort and keep only the first 'count' numbers
    reversible_squares.sort()
    return reversible_squares[:count]

# Find the first 50 reversible prime squares
result = find_reversible_prime_squares(50)

print("First 50 reversible prime squares:")
for i, num in enumerate(result, 1):
    prime = int(num**0.5)
    print(f"{i}. {num} (square of prime {prime})")

print(f"\nSum of the first 50 reversible prime squares: {sum(result)}")