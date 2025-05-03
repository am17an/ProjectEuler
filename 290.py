import collections
import time

def count_equal_sum_digits(L):
    """
    Counts the number of positive integers N with exactly L digits
    such that sd(N) = sd(137 * N).

    Args:
        L: The exact number of digits N must have.

    Returns:
        The count of such numbers N.
    """
    if L <= 0:
        return 0

    # dp[k] stores states reachable after processing k digits (d_0 to d_{k-1})
    # dp[k] = map from state tuple to map of {diff: count}
    # state tuple = (carry_in_k, d_{k-1}, d_{k-2})
    # diff = sum(d_i for i < k) - sum(p_i for i < k)
    # count = number of ways to reach this state with this difference
    dp = [collections.defaultdict(lambda: collections.defaultdict(int)) for _ in range(L + 1)]

    # Base case: k=0 (before processing any digits)
    # State: (carry_in=0, d_{-1}=0, d_{-2}=0)
    # Result: diff=0, count=1 (representing the empty prefix)
    dp[0][(0, 0, 0)][0] = 1

    # Maximum possible carry into the next column during multiplication
    # Estimated based on max value of Ck + 7*9 + 3*9 + 1*9 = Ck + 99
    # If Ck maxes out around 10, next carry is floor(109/10)=10. Use 11 for safety.
    MAX_CARRY = 11

    # --- Dynamic Programming Loop ---
    # Iterate through each digit position k from 0 (units) to L-1 (most significant)
    for k in range(L):
        # print(f"Processing k={k}, number of states = {len(dp[k])}") # Debug
        for state, diff_counts in dp[k].items():
            Ck, dk_1, dk_2 = state # Ck is carry into column k, dk_1=d_{k-1}, dk_2=d_{k-2}

            for diff, count in diff_counts.items():
                if count == 0: # Skip if count is zero
                    continue

                # Try assigning each possible digit (0-9) to position k (dk)
                for dk in range(10):
                    # --- Constraint: Handle Leading Zeros ---
                    # If this is the most significant digit (k=L-1)
                    # and the digit is 0, it's not an L-digit number (unless L=1).
                    if k == L - 1 and dk == 0 and L > 1:
                        continue

                    # --- Simulation: Calculate Product Digit pk and Next Carry Ck+1 ---
                    # This simulates column k of the standard multiplication N * 137
                    if k == 0: # Units column
                        # Sum = Ck(=0) + 7*dk + 3*d_{-1}(=0) + 1*d_{-2}(=0)
                        val = 7 * dk
                    elif k == 1: # Tens column
                        # Sum = Ck + 7*dk + 3*dk_1(=d0) + 1*d_{-1}(=0)
                        val = Ck + 7 * dk + 3 * dk_1
                    else: # Hundreds column and onwards
                        # Sum = Ck + 7*dk + 3*dk_1(=d_{k-1}) + 1*dk_2(=d_{k-2})
                        val = Ck + 7 * dk + 3 * dk_1 + 1 * dk_2

                    pk = val % 10  # The k-th digit of the product 137*N
                    Ck1 = val // 10 # The carry into column k+1

                    # Optional sanity check for carry bounds
                    if Ck1 >= MAX_CARRY:
                       # This indicates MAX_CARRY might be too small,
                       # though 11 should be sufficient.
                       # print(f"Warning: Carry {Ck1} exceeded MAX_CARRY at k={k}, state={state}, dk={dk}")
                       continue

                    # --- Update State and Difference ---
                    # Calculate the difference for the next state (k+1)
                    # diff_{k+1} = diff_k + dk - pk
                    new_diff = diff + dk - pk

                    # Define the next state tuple for dp[k+1]
                    # (carry into k+1, digit at k, digit at k-1)
                    next_state = (Ck1, dk, dk_1)

                    # Add the counts to the next state in dp[k+1]
                    dp[k+1][next_state][new_diff] += count

    # --- Final Count Calculation ---
    total_count = 0
    # Iterate through all states reached after processing L digits (k=L)
    for state, diff_counts in dp[L].items():
        final_carry, dL_1, dL_2 = state # C_L, d_{L-1}, d_{L-2}

        # --- Account for Final Product Digits ---
        # The multiplication N * 137 might produce digits beyond p_{L-1}.
        # These digits (pL, pL+1, pL+2) depend on the final state.
        # We need to calculate them and their sum.

        # Column L: Sum = C_L + 7*0 + 3*d_{L-1} + 1*d_{L-2}
        val_L = final_carry + 3 * dL_1 + 1 * dL_2
        pL = val_L % 10
        CL1 = val_L // 10 # Carry into column L+1

        # Column L+1: Sum = C_{L+1} + 7*0 + 3*0 + 1*d_{L-1}
        val_L1 = CL1 + 1 * dL_1
        pL1 = val_L1 % 10
        CL2 = val_L1 // 10 # Carry into column L+2

        # Column L+2: Sum = C_{L+2} + 7*0 + 3*0 + 1*0
        val_L2 = CL2
        pL2 = val_L2 % 10
        CL3 = val_L2 // 10 # Carry into column L+3

        # The multiplication is fully accounted for if the final carry CL3 is 0.
        # This should always be true based on analysis.
        if CL3 == 0:
            # The target difference we need is the sum of these final product digits.
            # We require diff_L == pL + pL1 + pL2
            target_diff = pL + pL1 + pL2

            # Check if this target difference exists for the current state
            if target_diff in diff_counts:
                 total_count += diff_counts[target_diff]

    # Note: This counts positive integers N. sd(0)=0 and sd(137*0)=0,
    # but N=0 is not an L-digit number for L>=1.

    return total_count

# --- Example Usage ---
max_digits = 7# Set the desired number of digits L
start_time = time.time()
count = count_equal_sum_digits(max_digits)
end_time = time.time()

print(f"Number of positive integers N with exactly {max_digits} digits such that sd(N) = sd(137*N): {count}")
print(f"Calculation took: {end_time - start_time:.4f} seconds")

# --- Verification for small L ---
# L=1: N=9. sd(9)=9. 137*9=1233, sd(1233)=9. Count=1.
# L=2: N=90, N=99.
#   N=90: sd(90)=9. 137*90=12330, sd(12330)=9.
#   N=99: sd(99)=18. 137*99=13563, sd(13563)=18. Count=2.
# L=3: N=900, 909, 990, 999.
#   N=900: sd=9. 137*900=123300, sd=9.
#   N=909: sd=18. 137*909=124533, sd=18.
#   N=990: sd=18. 137*990=135630, sd=18.
#   N=999: sd=27. 137*999=136863, sd=27. Count=4.

print("\nVerifying for small L:")
for l in range(1, 8):
    print(f"L={l}: Count = {count_equal_sum_digits(l)}")


