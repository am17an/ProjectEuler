from math import gcd, isqrt
from collections import Counter
import sympy

def count_representations(n, method="direct"):
    """Count the number of ways to express n as a sum of two squares."""
    if method == "direct":
        # Direct counting method
        count = 0
        for a in range(isqrt(n) + 1):
            b_squared = n - a**2
            if b_squared >= 0:
                b = isqrt(b_squared)
                if b**2 == b_squared:
                    count += 1
        return count
    elif method == "formula":
        # Theoretical formula based on prime factorization
        # This requires the prime factorization of n
        if n == 0:
            return 1
        
        # Get prime factorization
        factors = sympy.factorint(n)
        
        # Apply the formula for number of representations
        result = 1
        for p, e in factors.items():
            if p == 2:
                # Prime p = 2 doesn't affect the count
                continue
            if p % 4 == 3:
                # Primes of form 4k+3 must have even exponent
                if e % 2 == 1:
                    return 0
            elif p % 4 == 1:
                # Primes of form 4k+1 contribute (e+1) to the count
                result *= (e + 1)
        
        # Adjust for powers of 2
        if 2 in factors:
            e = factors[2]
            if n % 4 == 0:  # n is divisible by 4
                result *= (e + 1)
            # else: e doesn't affect the result
        
        return result

def circle_points(n_max=1000):
    results = []
    
    for n in range(1, n_max + 1):
        # For the circle (x-N/2)² + (y-N/2)² = N²/2
        # We need to find integer solutions to u² + v² = 2N²
        # where u = 2x-N and v = 2y-N
        
        target = 2 * n**2
        
        # Count representations of target as sum of two squares
        reps = count_representations(target, "formula")
        
        # Each representation gives multiple integer points on the circle
        # Depending on symmetry
        
        # For each representation (a,b) of target as a²+b²=target,
        # we need to check if it gives integer (x,y)
        
        count = 0
        if n % 2 == 0:  # N is even
            # Integer points happen when u,v are both even
            # Each representation gives at most 4 points (±a,±b)
            even_reps = 0
            for a in range(0, isqrt(target) + 1, 2):  # Even values only
                b_squared = target - a**2
                if b_squared >= 0:
                    b = isqrt(b_squared)
                    if b**2 == b_squared and b % 2 == 0:  # Perfect square and even
                        if a == 0 or b == 0:
                            even_reps += 1  # (a,0) or (0,b) gives 2 points
                        elif a == b:
                            even_reps += 1  # (a,a) gives 2 points
                        else:
                            even_reps += 2  # (a,b) and (b,a) give 4 points
            count = even_reps * 2  # Each even representation gives 2 points
        else:  # N is odd
            # Integer points happen when u,v are both odd
            # Each representation gives at most 4 points (±a,±b)
            odd_reps = 0
            for a in range(1, isqrt(target) + 1, 2):  # Odd values only
                b_squared = target - a**2
                if b_squared >= 0:
                    b = isqrt(b_squared)
                    if b**2 == b_squared and b % 2 == 1:  # Perfect square and odd
                        if a == b:
                            odd_reps += 1  # (a,a) gives 2 points
                        else:
                            odd_reps += 2  # (a,b) and (b,a) give 4 points
            count = odd_reps * 2  # Each odd representation gives 2 points
        
        results.append((n, count))
        
        if n % 100 == 0:
            print(f"Processed up to N = {n}")
    
    return results

# Run the analysis
results = circle_points(100)  # Reduced to 100 for brevity

# Show all results
print("\nResults:")
for n, count in results:
    print(f"N = {n}: {count} points")

# Analyze patterns
print("\nAnalyzing patterns...")
counts_by_mod5 = {i: [] for i in range(5)}
counts_by_mod10 = {i: [] for i in range(10)}

for n, count in results:
    counts_by_mod5[n % 5].append(count)
    counts_by_mod10[n % 10].append(count)

print("\nDistribution by n mod 5:")
for r, counts in counts_by_mod5.items():
    count_freq = Counter(counts)
    print(f"  n ≡ {r} (mod 5): {dict(count_freq)}")

print("\nDistribution by n mod 10:")
for r, counts in counts_by_mod10.items():
    count_freq = Counter(counts)
    print(f"  n ≡ {r} (mod 10): {dict(count_freq)}")