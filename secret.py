import numpy as np
from collections import defaultdict

def matrix_to_str(matrix):
    """Convert matrix to string representation for hash-based cycle detection"""
    return str(matrix.tolist())

def transform_matrix(matrix):
    """Transform matrix by replacing each cell with the sum of its four orthogonal neighbors"""
    rows, cols = matrix.shape
    new_matrix = np.zeros((rows, cols), dtype=object)
    
    for i in range(rows):
        for j in range(cols):
            # Get the four orthogonal neighbors with wrap-around
            top = matrix[(i - 1) % rows, j]
            bottom = matrix[(i + 1) % rows, j]
            left = matrix[i, (j - 1) % cols]
            right = matrix[i, (j + 1) % cols]
            
            # Sum the neighbors
            new_matrix[i, j] = (top + bottom + left + right)%7
    
    return new_matrix

def detect_cycle_and_transform(initial_matrix, target_iterations=10**12):
    """Detect cycle in matrix transformations and calculate final state"""
    # Convert input to numpy array with object dtype for arbitrary-precision integers
    matrix = np.array(initial_matrix, dtype=object)
    
    # Dictionary to store matrices we've seen and at which iteration
    seen_matrices = {}
    
    iterations = 0
    while iterations < target_iterations:
        # Create a hashable representation of the current matrix
        matrix_str = matrix_to_str(matrix)
        
        # Check if we've seen this matrix state before
        if matrix_str in seen_matrices:
            # We found a cycle!
            cycle_start = seen_matrices[matrix_str]
            cycle_length = iterations - cycle_start
            print(f"Cycle detected! Starts at iteration {cycle_start}, length {cycle_length}")
            
            # Calculate remaining iterations needed after cycles
            remaining_iterations = (target_iterations - iterations) % cycle_length
            
            # Apply the remaining iterations
            for _ in range(remaining_iterations):
                matrix = transform_matrix(matrix)
            
            return matrix
        
        # Store current matrix state
        seen_matrices[matrix_str] = iterations
        
        # Transform matrix
        matrix = transform_matrix(matrix)
        iterations += 1
        
        # Print progress every 100 iterations
        if iterations % 100 == 0:
            print(f"Completed {iterations} iterations...")
    
    return matrix

def get_secret_word(final_matrix):
    """Extract the secret word by taking each pixel modulo 7"""
    # Apply modulo 7 to get the secret values
    mod_matrix = np.mod(final_matrix, 7)
    
    # Map values 0-6 to characters (assuming 0=A, 1=B, etc.)
    char_mapping = {
        0: 'A', 1: 'B', 2: 'C', 3: 'D', 
        4: 'E', 5: 'F', 6: 'G'
    }
    
    # Convert the modulo values to characters
    secret_chars = []
    for row in mod_matrix:
        for cell in row:
            if cell != 0:  # Skip zeros if needed
                secret_chars.append(char_mapping[cell])
    
    return ''.join(secret_chars)

# Initial matrix from the problem
initial_matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 100],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [66, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [65, 69, 0, 0, 0, 0, 0, 0, 0, 67],
    [68, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 98],
    [101, 0, 0, 0, 0, 0, 0, 0, 99, 97],
]

# Find the final matrix after 10^12 iterations
final_matrix = detect_cycle_and_transform(initial_matrix, 10**12)

# Extract the secret word
secret_word = get_secret_word(final_matrix)
print(f"Secret word: {secret_word}")

# Alternative approach: We can also try printing the entire matrix mod 7
print("\nFinal Matrix (modulo 7):")
mod_matrix = np.mod(final_matrix, 7)
for row in mod_matrix:
    print(' '.join(map(str, row)))