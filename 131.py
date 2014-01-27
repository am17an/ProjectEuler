#define primes
import gmpy
pr = [2]
curr =2 
for i in range(1000):
    pr.append(gmpy.next_prime(curr))
    curr = gmpy.next_prime(curr)

#cubes 
cubes = [i**3 for i in range(1,1000)]
#squares
squares = [i**2 for i in range(1,1000)]

cubes = set(cubes).intersection(squares)

print cubes

for prime in pr:
    for i in cubes:
        if i + prime in cubes:
            print i,prime
            break
