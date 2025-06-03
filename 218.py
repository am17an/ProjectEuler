from sympy import primerange
from math import isqrt

def generate_sum_of_two_squares_squares(limit):
    primes = list(primerange(2, isqrt(limit) + 1))
    result = set()

    def dfs(idx, curr):
        if curr > limit:
            return
        if curr != 1 and isqrt(curr)**2 == curr:
            result.add(curr)
        for i in range(idx, len(primes)):
            p = primes[i]
            max_exp = 1
            while True:
                exp = 2 * max_exp  # only even exponents to keep result a square
                if p % 4 == 3 and exp % 2 != 0:
                    max_exp += 1
                    continue  # skip odd exponents for 4k+3 primes
                next_val = curr * (p ** exp)
                if next_val > limit:
                    break
                dfs(i + 1, next_val)
                max_exp += 1

    dfs(0, 1)
    return sorted(result)

# --- Usage ---
limit = int(1e16)
valid_squares = generate_sum_of_two_squares_squares(limit)
print(len(valid_squares))