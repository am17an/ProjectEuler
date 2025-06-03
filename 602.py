mod = int(1e9 + 7)

def pow_mod(x, n, mod):
    result = 1
    while n > 0:
        if n % 2 == 1:
            result = (result * x) % mod
        x = (x * x) % mod
        n //= 2
    return result

def calculate(N, K):
    # Precompute binomial coefficients C(N+1, i) for i from 0 to K
    binom = [0] * (K + 1)
    binom[0] = 1
    
    for i in range(1, K + 1):
        # Using the formula C(n,k) = C(n,k-1) * (n-k+1) / k
        binom[i] = (binom[i-1] * (N + 1 - (i - 1)) % mod * pow_mod(i, mod - 2, mod)) % mod
    
    # Calculate Eulerian number using precomputed binomial coefficients
    result = 0
    for i in range(K + 1):
        term = binom[i]
        if i % 2 == 1:
            term = mod - term  # Equivalent to multiplying by -1
        term = (term * pow_mod(K + 1 - i, N, mod)) % mod
        result = (result + term) % mod
    
    return result


print(calculate(10000000, 4000000-1))