from sympy import isprime, divisors, sieve
from math import isqrt


squares = []
limit = int(1e8)
#limit = int(100)

sieve.extend(limit)

for i in sieve.primerange(limit):
    squares.append((i+1)**2)

print(len(squares))

total = 0
for sq in squares:

    divs = divisors(sq)
    for i in range(len(divs)//2):
        d = divs[i]
        if sq//d -1 <= limit and d-1 in sieve and sq//d - 1 in sieve:
                #print(d-1, sq//d -1, isqrt(sq)-1, sq)
            total += d-1 
            total += sq//d - 1
            total += isqrt(sq) - 1


print(total)