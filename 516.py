from sympy import totient, primefactors,isprime,divisors
numbers = set()

for i in range(1, 101):
    if len(divisors(i))%7 == 0:
        print(i)
    
    