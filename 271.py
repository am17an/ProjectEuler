from sympy import primerange
from sympy.ntheory.modular import crt

# First 14 primes
primes = list(primerange(1, 44))  # 2 to 43
moduli = primes

print(primes)
# Function to compute cube roots of unity mod p
def cube_roots_mod_p(p):
    return [x for x in range(1, p) if pow(x, 3, p) == 1]

# Compute cube roots for each prime modulus
roots_mod_p = [cube_roots_mod_p(p) for p in moduli]

# Use product to compute all combinations
from itertools import product

all_combinations = list(product(*roots_mod_p))

# Apply CRT to get cube roots modulo N
results = set()
moduli_product = 1
for p in moduli:
    moduli_product *= p

for root_tuple in all_combinations:
    x, _ = crt(moduli, list(root_tuple))
    results.add(x % moduli_product)

# Output the count and first few cube roots
print(results)
print(sum(set(results)))