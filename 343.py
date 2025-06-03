import math

from sympy import primefactors,factorint

def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0:2] = [False, False]
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i, val in enumerate(is_prime) if val]


def factor(x):
    for i in range(2, int(math.isqrt(x)) + 1):
        while x % i == 0:
            yield i
            x //= i
    if x > 1:
        yield x

def largest_prime_divisor(n):
    a = n
    primes = sieve(int(a ** 0.5) + 1)

    print(primes)

    for i in range(len(primes)):
        if n%primes[len(primes)-i-1] == 0:
            return primes[len(primes)-i-1]

    return n

total = 1
for i in range(2*1000000, 2*1000000 + 1):
    if i%100000 == 0:
        print("Done", i)
    total += max(max(factorint(i+1)), max(factorint(i*i - i + 1))) - 1

print(total)


