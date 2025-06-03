from sympy import divisors, gcd
from math import gcd

N = 60
def order_mod(a, n):
    if gcd(a, n) != 1:
        return 0
    for k in sorted(divisors(N)):
        if pow(a, k, n) == 1:
            return k
    return 0

MOD_EXP = N
target = 2**MOD_EXP - 1

valid_m = []
for d in divisors(target):
    if d % 2 == 1 and gcd(2, d) == 1:
        if order_mod(2, d) == MOD_EXP:
            valid_m.append((d - 1) // 2)

print(sum([2*n+2 for n in valid_m]))
