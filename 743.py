import itertools

MOD = 10**9 + 7

# Set the maximum k you will ever need
MAX_K = 10**8

# Global arrays for factorial and inverse
fact = [1] * (MAX_K + 1)
inv = [1] * (MAX_K + 1)
_precomputed = False

def precompute_factorials(n, mod):
    global _precomputed
    if _precomputed:
        return
    for i in range(1, n+1):
        fact[i] = fact[i-1] * i % mod
    inv[n] = pow(fact[n], mod-2, mod)
    for i in range(n-1, -1, -1):
        inv[i] = inv[i+1] * (i+1) % mod
    _precomputed = True

def comb(n, k, mod):
    if k < 0 or k > n:
        return 0
    return fact[n] * inv[k] % mod * inv[n-k] % mod

def solve(n, k):
    precompute_factorials(k, MOD)
    print("Done with factorial")
    ans = pow(2, n, MOD)
    for ones in range(1, k//2 + 1):
        ans += comb(k, ones, MOD) * comb(k-ones, ones, MOD) * pow(2, (k-2*ones)*(n//k), MOD)
        ans %= MOD
    return ans

print(solve(10**16, 10**8))
