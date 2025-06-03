
from sympy import gcd


prev = 13
for i in range(5,1001):

    next = prev + gcd(i, prev)
    print(i, next, next-prev)

    prev = next
