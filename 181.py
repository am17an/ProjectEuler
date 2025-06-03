import functools

# --- 1. Integer Partition Function p(n) ---
@functools.lru_cache(maxsize=None)
def integer_partition_p(n):
    """
    Calculates the number of partitions of an integer n, p(n).
    Uses Euler's pentagonal number theorem recurrence.
    p(n) = p(n-1) + p(n-2) - p(n-5) - p(n-7) + ...
    p(0) = 1
    p(k) = 0 for k < 0
    """
    if n < 0:
        return 0
    if n == 0:
        return 1
    
    total_sum = 0
    k = 1
    while True:
        # Pentagonal numbers: k(3k-1)/2 and k(3k+1)/2
        pent1 = k * (3 * k - 1) // 2
        pent2 = k * (3 * k + 1) // 2
        
        term_val1 = 0
        if n - pent1 >= 0:
            term_val1 = integer_partition_p(n - pent1)
        else: # Subsequent terms will also be >= n
            break 
            
        term_val2 = 0
        if n - pent2 >= 0:
            term_val2 = integer_partition_p(n - pent2)

        if k % 2 == 1: # k is odd
            total_sum += term_val1 + term_val2
        else: # k is even
            total_sum -= term_val1 + term_val2
        
        # Optimization: if pent1 > n, no need to continue further for k either
        # This is handled by the n - pent1 >= 0 check already.
        # If term_val1 was 0 because n - pent1 < 0, then n - pent2 will also be < 0 for larger k
        # and for the current k, pent2 > pent1.
        
        k += 1
        
    return total_sum

# Alternative p(n) using simpler DP (often easier to reason about for smaller N)
# @functools.lru_cache(maxsize=None)
# def integer_partition_p_dp(n):
#     if n < 0: return 0
#     if n == 0: return 1
#     dp = [0] * (n + 1)
#     dp[0] = 1
#     for i in range(1, n + 1):      # Part size
#         for j in range(i, n + 1):  # Number being partitioned
#             dp[j] += dp[j - i]
#     return dp[n]


# --- 2. Sigma_q Function ---
# We will precompute Sigma_q values to avoid repeated calculations inside the main loop.
# sigma_q_table[kx][ky] will store Sigma_q(kx, ky)

def precompute_sigma_q(X_max, Y_max):
    """
    Precomputes Sigma_q(k_x, k_y) for 0 <= k_x <= X_max, 0 <= k_y <= Y_max.
    Sigma_q(K,L) = sum {a | m*a = K, m*b = L for some m>=1, and base part a+bi is first-quadrant non-zero}
    """
    sigma_q_table = [[0] * (Y_max + 1) for _ in range(X_max + 1)]

    for kx in range(X_max + 1):
        for ky in range(Y_max + 1):
            if kx == 0 and ky == 0:
                continue # Sigma_q(0,0) is not used in the sum (k_x,k_y)!=(0,0)

            current_sum_a = 0
            # Iterate m from 1.
            # The largest m can be is kx (if kx > 0) or ky (if ky > 0)
            # If kx=0, m can go up to ky. If ky=0, m can go up to kx.
            # If kx > 0 and ky > 0, m can go up to min(kx, ky) if we want a>0,b>0.
            # But parts can be purely real (b=0) or purely imaginary (a=0).
            limit_m = 1
            if kx > 0 : limit_m = max(limit_m, kx)
            if ky > 0 : limit_m = max(limit_m, ky)


            for m in range(1, limit_m + 1):
                if kx % m == 0 and ky % m == 0:
                    a = kx // m
                    b = ky // m
                    # Base part a+bi must be first-quadrant non-zero
                    if a >= 0 and b >= 0 and not (a == 0 and b == 0):
                        current_sum_a += a
            sigma_q_table[kx][ky] = current_sum_a
    return sigma_q_table


# --- 3. Main p_G Calculation Function ---
def calculate_p_G(X_target, Y_target):
    """
    Calculates p_G(X,Y), the number of partitions of X+iY into
    first-quadrant Gaussian integers.
    Uses the recurrence:
    X * p_G(X,Y) = sum_{k_x=0..X, k_y=0..Y, (k_x,k_y)!=(0,0)} Sigma_q(k_x,k_y) * p_G(X-k_x, Y-k_y)
    """
    if X_target < 0 or Y_target < 0:
        return 0

    # dp_table[x][y] will store p_G(x,y)
    dp_table = [[0] * (Y_target + 1) for _ in range(X_target + 1)]

    print("Precomputing Sigma_q values...")
    sigma_q_table = precompute_sigma_q(X_target, Y_target)
    print("Sigma_q precomputation complete.")

    # Base case: p_G(0,0) = 1
    dp_table[0][0] = 1

    # Base cases for the axes:
    # p_G(x,0) = p(x) (partitions of real x into real positive integers)
    print("Calculating base cases p_G(x,0)...")
    for x in range(1, X_target + 1):
        dp_table[x][0] = integer_partition_p(x)

    # p_G(0,y) = p(y) (partitions of iy into i*positive_integers)
    print("Calculating base cases p_G(0,y)...")
    for y in range(1, Y_target + 1):
        dp_table[0][y] = integer_partition_p(y)
    
    print("Base cases for axes complete.")

    # Fill the dp_table using the recurrence
    # Iterate x_current from 0, but only calculate if x_current > 0 or y_current > 0
    # The recurrence X * p_G(X,Y) is used, so X (x_current) must be > 0.
    # If x_current = 0, p_G(0,Y) is already filled.
    
    print("Starting main DP calculation...")
    for x_current in range(X_target + 1):
        for y_current in range(Y_target + 1):
            if x_current == 0 and y_current == 0:
                continue # p_G(0,0) is set
            if x_current == 0: # p_G(0, y_current) is already set as p(y_current)
                continue
            # If y_current == 0, p_G(x_current, 0) is already set as p(x_current)
            # This is fine, we can still calculate it using the recurrence to verify,
            # or just use the precomputed if y_current == 0. Let's calculate it for x_current > 0.
            
            if (x_current*10 // X_target) > ((x_current-1)*10 // X_target if X_target > 0 else 0) : # Progress update
                 print(f"  Calculating for x_current = {x_current} / {X_target}")


            current_sum_for_recurrence = 0
            for k_x in range(x_current + 1):
                for k_y in range(y_current + 1):
                    if k_x == 0 and k_y == 0:
                        continue # This term is excluded from the sum

                    # Term is sigma_q_table[k_x][k_y] * dp_table[x_current - k_x][y_current - k_y]
                    sigma_val = sigma_q_table[k_x][k_y]
                    prev_p_G_val = dp_table[x_current - k_x][y_current - k_y]
                    
                    current_sum_for_recurrence += sigma_val * prev_p_G_val
            
            # Recurrence: x_current * p_G(x_current, y_current) = current_sum_for_recurrence
            # So, p_G(x_current, y_current) = current_sum_for_recurrence / x_current
            # Since x_current > 0 here, division is safe.
            if x_current > 0 : # This condition is guaranteed by the outer loop structure
                 dp_table[x_current][y_current] = current_sum_for_recurrence // x_current
            # else:
                 # This 'else' branch for x_current = 0 should not be reached if loops are structured
                 # to rely on dp_table[0][y] = p(y)
                 # If it were reached, it would imply 0 * p_G(0,y) = sum, which means sum must be 0.
                 # This code path is avoided by how dp_table[0][y] is pre-filled.
                 pass


    print("DP calculation complete.")
    return dp_table[X_target][Y_target]

# --- Example Usage ---
if __name__ == "__main__":
    # Test integer_partition_p
    # print(f"p(5) = {integer_partition_p(5)}") # Expected: 7
    # print(f"p(10) = {integer_partition_p(10)}") # Expected: 42
    
    # Test Sigma_q precomputation
    # test_sigma_q = precompute_sigma_q(3,1)
    # print(f"Sigma_q(1,0) = {test_sigma_q[1][0]}") # Expected: 1
    # print(f"Sigma_q(2,0) = {test_sigma_q[2][0]}") # Expected: 1+2=3
    # print(f"Sigma_q(3,0) = {test_sigma_q[3][0]}") # Expected: 1+3=4
    # print(f"Sigma_q(0,1) = {test_sigma_q[0][1]}") # Expected: 0
    # print(f"Sigma_q(1,1) = {test_sigma_q[1][1]}") # Expected: 1
    # print(f"Sigma_q(2,1) = {test_sigma_q[2][1]}") # Expected: 2
    # print(f"Sigma_q(3,1) = {test_sigma_q[3][1]}") # Expected: 3

    # Test small p_G values
    # print(f"p_G(1,1) = {calculate_p_G(1,1)}") # Expected: 2
    # print(f"p_G(2,1) = {calculate_p_G(2,1)}") # Expected: 4
    # print(f"p_G(2,2) = {calculate_p_G(2,2)}") # Expected: 9
    # print(f"p_G(3,1) = {calculate_p_G(3,1)}") # Expected: 7
    
    # Calculate for a larger value like 60+40i
    # This will take some time.
    target_X = 10 # Reduced for quicker testing. Change to 60 for the original request.
    target_Y = 5  # Reduced for quicker testing. Change to 40 for the original request.

    # target_X = 60 
    # target_Y = 40 

    print(f"\nCalculating p_G({target_X}, {target_Y})...")
    result = calculate_p_G(target_X, target_Y)
    print(f"\nNumber of partitions p_G({target_X} + {target_Y}i) = {result}")

    # Example for p_G(4,0) = p(4) = 5
    # print(f"p_G(4,0) = {calculate_p_G(4,0)}")
    # Example for p_G(0,4) = p(4) = 5
    # print(f"p_G(0,4) = {calculate_p_G(0,4)}")