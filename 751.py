from decimal import Decimal, getcontext
import numpy as np

# Set precision to 50 decimal places
getcontext().prec = 50

def generate_sequence(theta, length):
    """Generate the sequence given theta"""
    if isinstance(theta, float):
        theta = Decimal(str(theta))
    
    b = [None, theta]  # b is 1-indexed in the problem
    a = [None]  # a is 1-indexed in the problem
    
    for n in range(1, length + 1):
        a.append(int(b[n]))  # Floor function
        if n < length:
            b.append(int(b[n]) * (b[n] - int(b[n]) + Decimal('1')))
    
    return a[1:]  # Return without the None at index 0

def compute_tau(sequence):
    """Compute the concatenation value tau"""
    first_element = sequence[0]
    rest = ''.join(map(str, sequence[1:]))
    return Decimal(f"{first_element}.{rest}")

# Example from the problem
theta_example = Decimal('2.956938891377988')
fib_sequence = generate_sequence(theta_example, 10)
print(f"Sequence for theta = {theta_example}:")
print(fib_sequence)

tau_example = compute_tau(fib_sequence)
print(f"Tau = {tau_example}")
print(f"Theta = {theta_example}")
print(f"Difference = {abs(tau_example - theta_example)}")

# Explore theta values that start with a_1 = 2
print("\nExploring theta values that start with a_1 = 2:")

test_values = [
    Decimal('2.3'),
    Decimal('2.35'),
    Decimal('2.357'),
    Decimal('2.358'),
    Decimal('2.359'),
    Decimal('2.36')
]

for theta in test_values:
    sequence = generate_sequence(theta, 15)
    if sequence[0] == 2:
        tau = compute_tau(sequence)
        print(f"For theta = {theta:.6f}, sequence: {', '.join(map(str, sequence[:8]))}...")
        print(f"Tau = {tau:.6f}, Difference = {abs(tau - theta):.6f}")

def find_fixed_point(initial_guess, precision=Decimal('1e-25'), max_iterations=50):
    """Numerically search for the fixed point"""
    if isinstance(initial_guess, float):
        theta = Decimal(str(initial_guess))
    else:
        theta = initial_guess
    
    iteration = 0
    best_theta = None
    best_diff = Decimal('Infinity')
    sequence_lengths = [100, 200, 300, 400, 500]  # Increasing sequence lengths
    
    while iteration < max_iterations:
        # Use longer sequences as we get closer to the fixed point
        length_idx = min(iteration // 5, len(sequence_lengths) - 1)
        seq_length = sequence_lengths[length_idx]
        
        sequence = generate_sequence(theta, seq_length)
        if sequence[0] != 2:
            print("Warning: sequence doesn't start with 2")
            return None
        
        tau = compute_tau(sequence)
        diff = abs(tau - theta)
        
        print(f"Iteration {iteration}: ")
        print(f"  theta = {theta:.25f}")
        print(f"  tau   = {tau:.25f}")
        print(f"  diff  = {diff:.25f}")
        print(f"  sequence length: {seq_length}")
        
        # Keep track of best result
        if diff < best_diff:
            best_diff = diff
            best_theta = theta
        
        if diff < precision:
            break
        
        # Use tau as our next guess for theta
        theta = tau
        iteration += 1
    
    if iteration == max_iterations:
        print("Warning: reached maximum iterations without converging")
        print(f"Using best approximation found (diff: {best_diff})")
        theta = best_theta
    
    # Final estimate using a very long sequence
    print("\nGenerating final estimate with a very long sequence...")
    final_sequence = generate_sequence(theta, 1000)
    
    # Print the first several digits of the sequence to help verify
    print(f"Final sequence starts with: {', '.join(map(str, final_sequence[:25]))}...")
    
    # Compute tau with the longer sequence for better precision
    estimated_tau = compute_tau(final_sequence)
    print(f"Final theta estimate: {theta:.30f}")
    print(f"Final tau estimate:   {estimated_tau:.30f}")
    
    # Return the estimated fixed point
    return theta

# Find the fixed point starting from 2.35
fixed_point = find_fixed_point(Decimal('2.35'))
if fixed_point:
    # Format the result with exactly 24 decimal places as requested in the problem
    print(f"\nAnswer rounded to 24 decimal places: {fixed_point:.24f}")