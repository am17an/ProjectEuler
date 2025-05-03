import math
def Divisors_of(x):  # Find the divisors of a number
    divisors = []
    for i in range(1, int(math.sqrt(x)) + 1):
        if x % i == 0:
            divisors.append(i)
    return (divisors)

def compute():
    alexandrian_integers = []
    p = 1
    while len(alexandrian_integers) < 500000:
        for k in Divisors_of(p*p + 1):
            alexandrian_integers.append(p*(p + k)*((p*p + 1)//k + p))
        p += 1
    return sorted(alexandrian_integers)[149999]

print(compute())