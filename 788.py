MOD = 10**9 + 7

def precompute_factorials(n, mod):
    fact = [1] * (n+1)
    inv = [1] * (n+1)
    for i in range(1, n+1):
        fact[i] = fact[i-1] * i % mod
    inv[n] = pow(fact[n], mod-2, mod)
    for i in range(n-1, -1, -1):
        inv[i] = inv[i+1] * (i+1) % mod
    return fact, inv

def comb(n, k, fact, inv, mod):
    if k < 0 or k > n:
        return 0
    return fact[n] * inv[k] % mod * inv[n-k] % mod

def D(n):
    fact, inv = precompute_factorials(n, MOD)
    res = 0
    half = n // 2
    for d in range(1, 10):
        for k in range(half+1, n+1):
            # First digit is d
            ways1 = comb(n-1, k-1, fact, inv, MOD) * pow(9, n-k, MOD) % MOD
            # First digit is not d (but not 0)
            ways2 = 8 * comb(n-1, k, fact, inv, MOD) * pow(9, n-k-1, MOD) % MOD if n-k-1 >= 0 else 0
            res = (res + ways1 + ways2) % MOD
    # d = 0
    for k in range(half+1, n+1):
        # First digit cannot be 0, so pick k positions for 0 among n-1 (not first digit)
        ways = 9 * comb(n-1, k, fact, inv, MOD) * pow(9, n-k-1, MOD) % MOD if n-k-1 >= 0 else 0
        res = (res + ways) % MOD
    return res

def is_dominating(num):
    s = str(num)
    n = len(s)
    cnt = [0]*10
    for ch in s:
        cnt[int(ch)] += 1
    for d in range(10):
        if cnt[d] > n//2:
            return True
    return False

def brute_D_total(n):
    count = 0
    for digits in range(1, n+1):
        start = 10**(digits-1) if digits > 1 else 1
        end = 10**digits
        for x in range(start, end):
            if is_dominating(x):
                count += 1
    return count

def D_total(n):
    return sum(D(i) for i in range(1, n+1)) % MOD

if __name__ == "__main__":
    print("D_total(4) =", D_total(4))      # Should be 603
    print("D_total(10) =", D_total(10))    # Should be 21893256
    print("brute_D_total(4) =", brute_D_total(4))
    print("D_total(2022) =", D_total(2022))    # Should be 21893256
