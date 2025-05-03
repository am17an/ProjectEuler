import numpy as np

def compute_M(p, a):
    """Find minimal M where p's exponent in M! >= a"""
    low = p
    high = p * a  # Initial upper bound
    while low < high:
        mid = (low + high) // 2
        total = 0
        power = p
        while power <= mid:
            total += mid // power
            power *= p
        if total >= a:
            high = mid
        else:
            low = mid + 1
    return low

def main():
    limit = 10**8
    max_M = np.zeros(limit + 1, dtype=np.uint32)
    max_M[1] = 0  # M(1) = 0

    # Sieve of Eratosthenes to find primes
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            sieve[i*i : limit+1 : i] = False
    primes = np.nonzero(sieve)[0].tolist()

    # Process each prime and its powers
    print("Done primes")
    for p in primes:
        a = 1
        while True:
            p_power = p ** a
            if p_power > limit:
                break
            m = compute_M(p, a)
            # Update all multiples of p^a with maximum M
            max_M[p_power::p_power] = np.maximum(max_M[p_power::p_power], m)
            a += 1

    print(f"Total sum: {max_M.sum()}")

if __name__ == "__main__":
    main()
