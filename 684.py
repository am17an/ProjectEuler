def mod_pow(base, exp, mod):
    """Efficient modular exponentiation."""
    if exp == 0:
        return 1
    half = mod_pow(base, exp // 2, mod)
    if exp % 2 == 0:
        return (half * half) % mod
    else:
        return (half * half * base) % mod

def geometric_sum(a, r, n, mod):
    """
    Calculate sum of geometric series: a + a*r + a*r^2 + ... + a*r^(n-1) (mod mod)
    Using the formula: a * (1 - r^n) / (1 - r) (with modular arithmetic)
    """
    if n == 0:
        return 0
    
    # Calculate r^n mod mod
    r_n = mod_pow(r, n, mod)
    
    # Calculate (1 - r^n) mod mod
    numerator = (1 - r_n) % mod
    
    # Calculate modular inverse of (1 - r) mod mod using Fermat's Little Theorem
    # For a prime modulus, a^(mod-2) ≡ a^(-1) (mod mod)
    denominator_inv = mod_pow((1 - r) % mod, mod - 2, mod)
    
    # Calculate the final result
    result = (a * numerator * denominator_inv) % mod
    
    return result

def S_optimized(N, mod=10**9 + 7):
    """
    Highly optimized calculation of S(N) using mathematical properties.
    Avoids iterating through O(N/9) groups by using closed-form formulas.
    """
    if N <= 0:
        return 0
    
    result = 0
    
    # Process digits 1-9
    min_val = min(N, 9)
    sum_1_to_min = (min_val * (min_val + 1)) // 2
    result = (result + sum_1_to_min) % mod
    
    if N <= 9:
        return result
    
    # Calculate which group N falls into
    group_number = (N - 1) // 9 + 1
    
    # Instead of iterating through each group, use mathematical formulas
    # For complete groups 2 to group_number-1:
    
    if group_number > 2:
        full_groups = group_number - 2  # Number of complete groups after the first
        
        # For each group g (2 to group_number-1), we have:
        # Sum = 45*10^(g-1) + 9*(10^(g-1) - 1)
        
        # Let's separate this into two parts:
        
        # Part 1: Sum of 45*10^(g-1) for g=2 to group_number-1
        # This is 45 * (10^1 + 10^2 + ... + 10^(group_number-2))
        # This is a geometric series with first term a=45*10^1, ratio r=10, and n=full_groups
        part1 = (45 * geometric_sum(10, 10, full_groups, mod)) % mod
        
        # Part 2: Sum of 9*(10^(g-1) - 1) for g=2 to group_number-1
        # This simplifies to:
        # 9 * (sum of 10^(g-1) for g=2 to group_number-1) - 9 * full_groups
        # The sum is another geometric series
        part2_geo = geometric_sum(10, 10, full_groups, mod)
        part2 = (9 * part2_geo - 9 * full_groups) % mod
        
        # Add both parts to the result
        result = (result + part1 + part2) % mod
    
    # Process the last partial group
    if N > 9 * (group_number - 1):
        last_group = group_number
        start_n = 9 * (last_group - 1) + 1
        elements_in_last_group = N - start_n + 1
        
        # Sum of r from 1 to elements_in_last_group
        r_sum = (elements_in_last_group * (elements_in_last_group + 1)) // 2
        
        power = mod_pow(10, last_group-1, mod)
        
        # Sum of r*10^(last_group-1) for r=1 to elements_in_last_group
        digit_sum = (r_sum * power) % mod
        
        # Sum of (10^(last_group-1) - 1) * elements_in_last_group times
        nines_sum = (elements_in_last_group * ((power - 1) % mod)) % mod
        
        # Add contributions from last group
        last_group_sum = (digit_sum + nines_sum) % mod
        result = (result + last_group_sum) % mod
    
    return result

def fibonacci(n):
    """Generate the first n Fibonacci numbers (F1=1, F2=1, ...)."""
    fibs = [0, 1, 1]  # F0, F1, F2
    for i in range(3, n+1):
        fibs.append(fibs[i-1] + fibs[i-2])
    return fibs[1:]  # Return F1 through Fn

# Verification for S(20) = 1074
S_20 = S_optimized(20)
print(f"S(20) = {S_20}, Expected: 1074, Correct: {S_20 == 1074}")

# Calculate sum for first 10 Fibonacci numbers
fibs = fibonacci(10)
total_sum = 0
MOD = 10**9 + 7

print("\nCalculating S(Fi) for first 10 Fibonacci numbers:")
print("i | Fi | S(Fi)")
print("-" * 20)

for i, fib in enumerate(fibs, 1):
    if i >= 2:  # Starting from F2
        s_fi = S_optimized(fib, MOD)
        total_sum = (total_sum + s_fi) % MOD
        print(f"{i} | {fib:2d} | {s_fi}")

print(f"\nFinal sum for i=2 to 10: {total_sum}")

# For comparison, calculate sum for larger Fibonacci numbers
large_fibs = fibonacci(91)  # Using a smaller subset for demonstration
large_total = 0

print("\nDemonstrating efficiency with larger Fibonacci numbers:")
for i in range(2, 91):
    s_fi = S_optimized(large_fibs[i-1], MOD)
    large_total = (large_total + s_fi) % MOD
    if i % 5 == 0 or i <= 5:  # Print every 5th value and the first few
        print(f"i={i}, Fi={large_fibs[i-1]}, S(Fi)={s_fi}")

print(f"\nSum for i=2 to 90: {large_total}")