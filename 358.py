import math

def modinv(a, m):
    # Modular inverse using extended Euclidean algorithm
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = extended_gcd(b % a, a)
    return g, x - (b // a) * y, y

def starts_with(n, d, prefix):
    # Use logarithmic method to extract leading digits
    x = n * math.log10(10) - math.log10(d)
    frac = x - int(x)
    lead = int(10**(frac) * 1000)

    return lead//10 == prefix

def sieve_of_eratosthenes(limit):
    # Create a boolean array "prime[0..limit]" and initialize all entries as True.
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False  # 0 and 1 are not primes

    for p in range(2, int(limit**0.5) + 1):
        if prime[p]:
            # Marking multiples of p as False
            for i in range(p * p, limit + 1, p):
                prime[i] = False

    # Return all prime numbers up to the limit
    primes = [p for p in range(limit + 1) if prime[p]]
    return primes


def find_numbers(suffix=56789, prefix=137, limit=10**9):
    suffix_len = len(str(suffix))
    mod_base = 10 ** suffix_len
    primes = sieve_of_eratosthenes(limit)
    for n in primes:
        n -= 1
        d = n + 1
        # Check if (10^n - 1) % d == 0
        if (pow(10, n, d) - 1) % d != 0:
            continue
        # Compute ((10^n - 1)/d) % mod_base using modular arithmetic
        num_mod = (pow(10, n, d * mod_base) - 1) % (d * mod_base)
        inv_d = modinv(d, mod_base)
        if inv_d is None:
            continue
        result_mod = (num_mod * inv_d) % mod_base
        if result_mod != suffix:
            continue
        if starts_with(n, d, prefix):
            print(f"n = {n}, value ends with {suffix} and starts with {prefix}")

find_numbers()