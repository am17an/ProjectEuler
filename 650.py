"""
Project Euler Problem 650

For a positive integer n, let s(n) be the sum of all divisors of n.
For example, s(6) = 1 + 2 + 3 + 6 = 12.

Let S(n) = ∑ s(C(n,k)) for 0 ≤ k ≤ n, where C(n,k) is the binomial coefficient.
This can be simplified to the product of k^(2k - n - 1) for k from 0 to n.

We need to calculate S(n) modulo 10^9 + 7.

Known values:
S(5) = 5736
S(100) mod 10^9 + 7 = 332792866
"""

from functools import cache

@cache
def prime_factorization(n):
    """Return the prime factorization of n as a dictionary {prime: exponent}."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def mod_pow(base, exponent, modulus):
    """Calculate (base^exponent) % modulus efficiently."""
    if modulus == 1:
        return 0
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def mod_inverse(a, m):
    """Calculate the modular multiplicative inverse of a modulo m."""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def extended_gcd(a, b):
    """Extended Euclidean Algorithm to find gcd and coefficients."""
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def sum_of_geometric_series(a, r, n, mod):
    """Calculate (a + ar + ar^2 + ... + ar^n) % mod."""
    if r == 1:
        return (a * (n + 1)) % mod
    # Sum = a * (r^(n+1) - 1) / (r - 1)
    numerator = (mod_pow(r, n + 1, mod) - 1) % mod
    denominator = (r - 1) % mod
    return (a * numerator * mod_inverse(denominator, mod)) % mod

def S(n):
    """Calculate S(n) modulo 10^9 + 7."""
    MOD = 10**9 + 7
    
    # Store the prime factorization of the product
    prime_exponents = {}
    
    # For each k from 1 to n
    for k in range(1, n + 1):
        # Calculate the exponent for this k
        exponent = 2 * k - n - 1
        
        # Skip if the exponent is 0
        if exponent == 0:
            continue
        
        # Get prime factorization of k
        factors = prime_factorization(k)
        
        # Update the exponents in our overall factorization
        for prime, count in factors.items():
            prime_exponents[prime] = prime_exponents.get(prime, 0) + count * exponent
    
    # Calculate the sum of divisors
    result = 1
    for prime, exponent in prime_exponents.items():
        # Handle negative exponents (when 2k - n - 1 < 0)
        if exponent < 0:
            print("Negative exponent!", prime)
            # For p^(-e), we need to divide by p^e
            # This is equivalent to multiplying by the modular inverse of p^e
            inv_prime = mod_inverse(mod_pow(prime, -exponent, MOD), MOD)
            result = (result * inv_prime) % MOD
        else:
            # For each prime factor, calculate (p^0 + p^1 + ... + p^exponent)
            # This is a geometric series with a=1, r=prime, n=exponent
            term = sum_of_geometric_series(1, prime, exponent, MOD)
            result = (result * term) % MOD
    
    return result

# Test cases

ans = 0

for i in range(1, 20001):
    if i%1000 == 0:
        print(i)
    ans += S(i)
    ans %= int(1e9 + 7)

print(ans)

