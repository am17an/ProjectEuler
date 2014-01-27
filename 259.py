
import fractions

def gen(m, n):
    x = m
    r = set()
    for i in range(m + 1, n):
        for a in cache[(m, i)]:
            for b in cache[(i, n)]:
                r.add(a + b)
                r.add(a - b)
                r.add(a * b)
                if b:
                    if isinstance(a, int) and isinstance(b, int) and a % b == 0:
                        r.add(a // b)
                    else:
                        r.add(fractions.Fraction(a, b))
        x = x * 10 + i
    r.add(x)
    return r

nmax = 10

cache = {}
for l in range(1, nmax + 1):
    for i in range(1, nmax - l + 1):
        cache[(i, i + l)] = gen(i, i + l)

s = sum(x for x in cache[(1, nmax)]
        if x > 0 and (isinstance(x, int) or x.denominator == 1))
print(s)
