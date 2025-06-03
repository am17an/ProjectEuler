from math import isqrt

def generate_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, is_p in enumerate(sieve) if is_p]

def compute_S(n):
    primes = generate_primes(int(n ** (1/3)) + 10)
    S = 0

    def dfs(i, val):
        nonlocal S
        if val > n:
            return
        S += n // val
        for j in range(i, len(primes)):
            p = primes[j]
            if val * p**3 > n:
                break
            pw = p ** 3
            while val * pw <= n:
                dfs(j + 1, val * pw)
                pw *= p

    dfs(0, 1)
    return S

# Compute and print the result for s(10^18)
print(compute_S(int(1e18)))