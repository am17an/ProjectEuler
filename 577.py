def coefficient_of_x_power_n(n):
    """Calculate coefficient of x^n in 1/((1-x)^3*(1-x^3)^2)"""
    coeff = 0
    
    # Sum over all j such that 3j <= n
    for j in range(n // 3 + 1):
        i = n - 3 * j
        if i >= 0:
            # Coefficient from (1-x)^(-3) is C(i+2, 2) = (i+2)(i+1)/2
            # Coefficient from (1-x^3)^(-2) is (j+1)
            term = ((i + 2) * (i + 1) // 2) * (j + 1)
            coeff += term
    
    return coeff

def sum_coefficients(start, end):
    """Sum coefficients from x^start to x^end"""
    total = 0
    for n in range(start, end + 1):
        print(coefficient_of_x_power_n(n), n)
        total += coefficient_of_x_power_n(n)
    return total

# Calculate sum of coefficients from x^3 to x^12345
result = sum_coefficients(0, 12345-3)
print(f"Sum of coefficients from x^3 to x^12345: {result}")