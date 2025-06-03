#!/usr/bin/env python3

def matrix_multiply(A, B, mod):
    """Multiply two matrices A and B modulo mod"""
    n = len(A)
    m = len(B[0])
    k = len(B)
    
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for l in range(k):
                result[i][j] = (result[i][j] + A[i][l] * B[l][j]) % mod
    return result

def matrix_power(matrix, power, mod):
    """Compute matrix^power using binary exponentiation modulo mod"""
    n = len(matrix)
    
    # Initialize result as identity matrix
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    
    # Binary exponentiation
    base = [row[:] for row in matrix]  # Copy matrix
    
    while power > 0:
        if power & 1:
            result = matrix_multiply(result, base, mod)
        base = matrix_multiply(base, base, mod)
        power >>= 1
    
    return result

def solve_recurrence_matrix(n):
    """
    Solve the 23rd order recurrence using matrix exponentiation
    """
    MOD = 10**8 + 7
    
    # Initial values a(0) through a(23) - already mod MOD to avoid overflow
    initial_values = [
        1 % MOD,                          # a(0)
        229 % MOD,                        # a(1)
        117805 % MOD,                     # a(2)
        64647289 % MOD,                   # a(3)
        35669566217 % MOD,                # a(4)
        19690797527709 % MOD,             # a(5)
        10870506600976757 % MOD,          # a(6)
        6001202979497804657 % MOD,        # a(7)
        3313042830624031354513 % MOD,     # a(8)
        1829008840116358153050197 % MOD,  # a(9)
        1009728374600381843221483965 % MOD,              # a(10)
        557433823481589253332775648233 % MOD,            # a(11)
        307738670509229621147710358375321 % MOD,         # a(12)
        169891178715542584369273129260748045 % MOD,      # a(13)
        93790658670253542024618689133882565125 % MOD,    # a(14)
        51778366130057389441239986148841747669217 % MOD, # a(15)
        28584927722109981792301610403923348017948449 % MOD,              # a(16)
        15780685138381102545287108197623881881376915397 % MOD,           # a(17)
        8711934690116480171969789787256390490181022415693 % MOD,        # a(18)
        4809538076408327645969201260680362259835079086427481 % MOD,     # a(19)
        2655168723276120197512956906659822833388644760430125609 % MOD,  # a(20)
        1465820799640802552047402979496052449322258430218930512765 % MOD,           # a(21)
        809225642733724788155919446555896648357335949987871250500245 % MOD,         # a(22)
        446743654489197568088617503727278115945835626935048667406598225 % MOD       # a(23)
    ]
    
    # Coefficients for the recurrence relation (from a(n-1) to a(n-23))
    coefficients = [
        679, -76177, 3519127, -85911555, 1235863045, -11123194131, 
        65256474997, -257866595482, 705239311926, -1363115167354, 
        1888426032982, -1888426032982, 1363115167354, -705239311926, 
        257866595482, -65256474997, 11123194131, -1235863045, 
        85911555, -3519127, 76177, -679, 1
    ]
    
    if n <= 23:
        return initial_values[n]
    
    # Create transition matrix for the recurrence relation
    # State vector: [a(k), a(k-1), a(k-2), ..., a(k-22)]
    # Next state:   [a(k+1), a(k), a(k-1), ..., a(k-21)]
    
    transition_matrix = [[0] * 23 for _ in range(23)]
    
    # First row: coefficients of the recurrence relation
    for i in range(23):
        transition_matrix[0][i] = coefficients[i] % MOD
    
    # Other rows: shift previous values
    for i in range(1, 23):
        transition_matrix[i][i-1] = 1
    
    # Initial state vector: [a(23), a(22), a(21), ..., a(1)]
    initial_state = [initial_values[23-i] for i in range(23)]
    
    # Compute transition_matrix^(n-23)
    power = n - 23
    result_matrix = matrix_power(transition_matrix, power, MOD)
    
    # Multiply result_matrix with initial_state to get final state
    result = 0
    for i in range(23):
        result = (result + result_matrix[0][i] * initial_state[i]) % MOD
    
    return result

def solve_recurrence():
    """
    Solve the 23rd order recurrence relation for 3x3xN tower tiling (iterative method)
    """
    
    MOD = 10**8 + 7
    
    # Initial values a(0) through a(23)
    initial_values = [
        1,                          # a(0)
        229,                        # a(1)
        117805,                     # a(2)
        64647289,                   # a(3)
        35669566217,                # a(4)
        19690797527709,             # a(5)
        10870506600976757,          # a(6)
        6001202979497804657,        # a(7)
        3313042830624031354513,     # a(8)
        1829008840116358153050197,  # a(9)
        1009728374600381843221483965,              # a(10)
        557433823481589253332775648233,            # a(11)
        307738670509229621147710358375321,         # a(12)
        169891178715542584369273129260748045,      # a(13)
        93790658670253542024618689133882565125,    # a(14)
        51778366130057389441239986148841747669217, # a(15)
        28584927722109981792301610403923348017948449,              # a(16)
        15780685138381102545287108197623881881376915397,           # a(17)
        8711934690116480171969789787256390490181022415693,        # a(18)
        4809538076408327645969201260680362259835079086427481,     # a(19)
        2655168723276120197512956906659822833388644760430125609,  # a(20)
        1465820799640802552047402979496052449322258430218930512765,           # a(21)
        809225642733724788155919446555896648357335949987871250500245,         # a(22)
        446743654489197568088617503727278115945835626935048667406598225       # a(23)
    ]
    
    # Coefficients for the recurrence relation (from a(n-1) to a(n-23))
    coefficients = [
        679, -76177, 3519127, -85911555, 1235863045, -11123194131, 
        65256474997, -257866595482, 705239311926, -1363115167354, 
        1888426032982, -1888426032982, 1363115167354, -705239311926, 
        257866595482, -65256474997, 11123194131, -1235863045, 
        85911555, -3519127, 76177, -679, 1
    ]
    
    # Convert initial values to mod MOD
    a = [val % MOD for val in initial_values]
    
    print("Computing a(500) using 23rd order recurrence relation...")
    print(f"Initial values: a(0) = {a[0]}, a(1) = {a[1]}, a(2) = {a[2]}")

    # Compute values from a(24) to a(500)
    for n in range(24, 501):
        next_val = 0
        
        # Apply recurrence relation: a(n) = sum of coefficients[i] * a(n-1-i)
        for i in range(23):
            term = (coefficients[i] * a[n - 1 - i]) % MOD
            next_val = (next_val + term) % MOD
        
        a.append(next_val)
        
        # Print progress for some values
        if n % 50 == 0 or n <= 30:
            print(f"a({n}) = {next_val}")
    
    return a[500]

def verify_recurrence():
    """Verify the recurrence works with known values"""
    MOD = 10**8 + 7
    
    # Test with smaller known values
    initial_values = [1, 229, 117805, 64647289]
    coefficients = [679, -76177, 3519127, -85911555, 1235863045, -11123194131, 
                   65256474997, -257866595482, 705239311926, -1363115167354, 
                   1888426032982, -1888426032982, 1363115167354, -705239311926, 
                   257866595482, -65256474997, 11123194131, -1235863045, 
                   85911555, -3519127, 76177, -679, 1]
    
    print("Verifying recurrence relation...")
    print("This would require all 24 initial values to properly verify.")

if __name__ == "__main__":
    print("=== Testing Matrix Exponentiation ===")
    
    # Test with known values first
    test_values = [500, 1000, 2000]
    
    for n in test_values:
        result = solve_recurrence_matrix(n)
        print(f"a({n}) mod (10^8 + 7) = {result}")
    
    print("\n=== Computing for Very Large Value ===")
    
    # Compute for 5 * 10^9999
    large_n = 5 * (10 ** 9999)
    print(f"Computing a(5 * 10^9999)...")
    print(f"This is a number with approximately 10000 digits")
    
    import time
    start_time = time.time()
    result_large = solve_recurrence_matrix(large_n)
    end_time = time.time()
    
    print(f"a(5 * 10^9999) mod (10^8 + 7) = {result_large}")
    print(f"Computation time: {end_time - start_time:.4f} seconds")
    
    print("\n=== Verification with smaller values ===")
    # Verify matrix method matches iterative method for smaller values
    print("Comparing matrix vs iterative methods:")
    iterative_500 = solve_recurrence()
    matrix_500 = solve_recurrence_matrix(500)
    print(f"Iterative a(500): {iterative_500}")
    print(f"Matrix a(500): {matrix_500}")
    print(f"Methods match: {iterative_500 == matrix_500}") 