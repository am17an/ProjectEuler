from fractions import Fraction

def calculate_th_probability_mod_n(k, N):
    MOD = int(1e8)
    
    # Numerator and denominator are calculated using modular arithmetic,
    # consistent with how these types of problems are often approached when N is large.
    # Using the formula structure from your latest changes for the numerator.
    numerator = (pow(2, N - k, MOD) * (N - k + (k - 1) * pow(2, N, MOD) + 1)) % MOD
    denomator = pow((pow(2, N, MOD) - 1), 2, MOD) # This is ((pow(2,N,MOD)-1)^2)%MOD

    # The Fraction object will store this fraction in its simplest (reduced) form.
    return (numerator * denomator)%MOD

def gcd(a, b):
    """Calculate the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """Return gcd(a, b) and coefficients such that a*x + b*y = gcd(a,b)."""
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def mod_inverse(a, m):
    """Return the modular inverse of a modulo m."""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def compute_final_result(problems):
    """
    Compute the product of fractions modulo 10^8.
    
    Args:
        problems: List of (N, target_mod_val) pairs for each problem.
        
    Returns:
        int: Last 8 digits of the product of these fractions in reduced form.
    """
    MOD = int(1e8)
    final_product_mod_M = 1
    
    for N, target_mod_val in problems: # k is target_mod_val
        # calculate_th_probability_mod_n now always returns a Fraction object
        fraction_obj = calculate_th_probability_mod_n(k=target_mod_val, N=N)
        
        num = fraction_obj.numerator
        den = fraction_obj.denominator
        
        # Find modular inverse of the denominator for the current term
        # The Fraction object ensures num/den is already in reduced form.
        # Denominators from Fraction object can be large, mod_inverse handles den % MOD internally.
        den_inverse = mod_inverse(den, MOD)
        
        # Numerators from Fraction object can also be large, so take num % MOD.
        term_value_mod_M = ((num % MOD) * den_inverse) % MOD
        
        final_product_mod_M = (final_product_mod_M * term_value_mod_M) % MOD
    
    return final_product_mod_M

# Verification
# P(k=0, N=2)

# P(k=1, N=2) to check sum to 1
k1_N2 = calculate_th_probability_mod_n(k=1, N=2)
print(f"P(k=1, N=2): Expected 4/9, Got: {k1_N2}")

# P(k=2, N=6)
k2_N6 = calculate_th_probability_mod_n(k=10**4 + 7, N=10**8 + 7)
print(f"P(k=2, N=6): Expected 368/1323, Got: {k2_N6}")
print(f"P(k=2, N=6) actual: {calculate_th_probability_mod_n(k=2, N=6)}")

print(calculate_th_probability_mod_n(1, 3))
print(calculate_th_probability_mod_n(2, 6))


#problems = [(10**8 + 7, 10**4 + 7)]
#print(compute_final_result(problems=problems))



# Example: P(k=0, N=1)
# N=1 means k%1 == 0 always. So probability should be 1.
#k0_N1 = calculate_th_probability_mod_n(target_mod_val)