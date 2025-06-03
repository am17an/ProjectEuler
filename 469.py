import sys
from fractions import Fraction

# Increase recursion limit
sys.setrecursionlimit(int(1e9))

# Create a cache dictionary to store previously computed results
cache = {}

def f(n):
    # Check if result is in cache
    if n in cache:
        return cache[n]
    
    # Base cases
    if n == 1:
        cache[n] = 0
        return 1
    if n == 2:
        cache[n] = 1
        return 1
    if n == 3:
        cache[3] = 2
        return 2
    
    # For n >= 4, use recursion with the recurrence relation
    a = (n - 4) / (n - 3)
    b = 2 / (n - 3)
    
    result = a * f(n-1) + b * f(n-2)
    cache[n] = result

    return result

# Calculate f(10^7) directly
target = 10**7
print(f"Calculating f({target})...")

for i in range(4, 1000):
    print(f(i), i, f(i)/i)

