# sequence_solver.py
import sys

# Increase recursion depth limit for potentially deep calculations
# The required depth can grow depending on the structure of calls,
# especially for a_{2k+1} needing a_{k+1}.
try:
    # Set a generous limit, adjust if RecursionError still occurs.
    new_limit = 20000
    sys.setrecursionlimit(new_limit)
    # print(f"Recursion depth limit set to {sys.getrecursionlimit()}")
except Exception as e:
    print(f"Warning: Could not set recursion depth limit: {e}")

memo = {1: 1}
# history stores value -> first index n where value appeared
history = {1: 1} 
max_n_computed = 0
repeated_values_found = False

def compute_a(n):
    """
    Computes a_n using the recurrence relation with memoization.
    Also checks if the computed value has appeared before in the sequence.
    """
    global max_n_computed, repeated_values_found
    max_n_computed = max(max_n_computed, n)

    if n in memo:
        return memo[n]
    # Base case a_1=1 is handled by initial memo dictionary.
    # We should ensure n >= 1 is always called.
    if n <= 0:
        raise ValueError("n must be a positive integer")

    if n % 2 == 0:
        # n = 2k => k = n / 2
        k = n // 2
        result = 2 * compute_a(k)
    else:
        # n = 2k + 1 => k = (n - 1) / 2
        k = (n - 1) // 2
        # Need a_k and a_{k+1}
        # compute_a(k) should ideally be called before compute_a(k+1)
        # if k > 0, otherwise compute_a(0) would raise error.
        # k=0 only when n=1, which is memoized. So k is always >= 1 here.
        term_k = compute_a(k)
        term_k_plus_1 = compute_a(k + 1)
        result = term_k - 3 * term_k_plus_1

    memo[n] = result

    # Check for repeated values
    if result in history:
        if not repeated_values_found: # Print only the first time a repetition is found
             print(f"Value {result} first appeared at index {history[result]}, now reappears at index {n}. Potential cycle indicator.")
             repeated_values_found = True
        # You could add more logic here, e.g., store all occurrences
    else:
        history[result] = n

    return result

def calculate_S(N):
    """Calculates S(N) = sum_{n=1}^N a_n."""
    current_sum = 0
    print(f"Calculating S({N})...")
    for i in range(1, N + 1):
        # Ensure term is computed if not already
        term_i = compute_a(i)
        current_sum += term_i
        # Optional: print progress for large N
        # if i % (N // 10) == 0:
        #     print(f"Processed up to a_{i}, current sum S({i}) = {current_sum}")
    return current_sum

# --- Main execution ---

# Verify S(10)
N_sum = 10
s_N = calculate_S(N_sum)
print(f"S({N_sum}) = {s_N}")
if s_N == -13:
    print("S(10) matches the value given in the problem description.")
else:
    print(f"Warning: S(10) calculated as {s_N}, expected -13.")

# Compute more terms to check for cycles/patterns
# Adjust N_check as needed. Larger values require more memory and time.
N_check = 10000
print(f"\nComputing terms up to N = {N_check} to check for patterns/cycles...")

computation_interrupted = False
try:
    # We compute terms sequentially up to N_check.
    # compute_a handles recursive calls and memoization for dependencies.
    for i in range(1, N_check + 1):
         compute_a(i) # Ensure all terms up to N_check are computed and checked
except RecursionError:
    print(f"Recursion depth exceeded near n={max_n_computed + 1}. Current limit: {sys.getrecursionlimit()}.")
    print("Try increasing the recursion limit further if needed, or use an iterative approach.")
    computation_interrupted = True
except Exception as e:
     print(f"An error occurred during computation near n={max_n_computed + 1}: {e}")
     computation_interrupted = True

print(f"\nFinished computation attempt up to N = {N_check}.")
print(f"Maximum index n for which a_n was computed: {max_n_computed}")

if not computation_interrupted:
    # Display the last few terms if computation completed
    print("\nLast 10 computed terms:")
    start_idx = max(1, N_check - 9)
    for i in range(start_idx, N_check + 1):
         print(f"a_{i} = {memo.get(i, 'Not computed')}")

# Report on cycle check findings
if not repeated_values_found:
    print("\nNo repeated values found in the sequence up to the maximum computed term.")
else:
     print("\nRepeated values were found (see messages above). This might indicate a cycle or just coincidental value repetition.")

# Check if 0 appeared
if 0 in history:
    print(f"\nSequence value 0 first appeared at index {history[0]}.")
else:
    print("\nSequence value 0 was not encountered.")

# You can add more analysis here, e.g., plot the sequence, check growth rate, etc. 