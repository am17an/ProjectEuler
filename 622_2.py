def find_order(base, modulus):
    """Find multiplicative order of base modulo modulus"""
    if modulus == 1:
        return 1
    
    m = 1
    power = base % modulus
    
    while power != 1:
        power = (power * base) % modulus
        m += 1
    
    return m

n = 52
modulus = 2*n - 1  # 103
result = find_order(2, modulus)
print(f"For n={n}, modulus={modulus}, s(n) = {result}")

# Let's also find all n where s(n) = 8
results = []
for n in range(2, 100):
    modulus = 2*n - 1
    if find_order(2, modulus) == 8:
        results.append(n)

print(f"\nAll values of n where s(n) = 8:")
for n in results:
    print(f"n = {n}")
