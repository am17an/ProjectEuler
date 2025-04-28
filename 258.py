import numpy as np
from scipy import sparse

# Define constants
SIZE = 2000
MOD = 20092010

def create_sparse_matrix():
    """Create the sparse matrix for the recurrence relation."""
    # Create the sparse matrix using coordinate format (COO)
    row_indices = []
    col_indices = []
    values = []
    
    # Add the two ones in the first column
    row_indices.extend([SIZE-1, SIZE-2])
    col_indices.extend([0, 0])
    values.extend([1, 1])
    
    # Add the shifted diagonal ones
    for i in range(SIZE-1):
        row_indices.append(i)
        col_indices.append(i+1)
        values.append(1)
    
    # Create the sparse matrix
    return sparse.csr_matrix((values, (row_indices, col_indices)), shape=(SIZE, SIZE))

def sparse_matrix_multiply_mod(A, B, mod):
    """Multiply two sparse matrices with modular arithmetic."""
    C = A @ B
    # Apply modulo to non-zero elements
    C.data %= mod
    return C

def sparse_matrix_expo(matrix, n):
    """Compute matrix^n using binary exponentiation with sparse matrices."""
    result = matrix.copy()
    power = matrix.copy()
    n -= 1  # Adjust because we start with result = matrix
    
    while n > 0:
        print(f"Remaining power: {n}")
        if n % 2 == 1:
            result = sparse_matrix_multiply_mod(result, power, MOD)
        power = sparse_matrix_multiply_mod(power, power, MOD)
        n //= 2
    
    return result

def main():
    # Create the sparse matrix
    matrix = create_sparse_matrix()
    
    # Compute matrix^20000
    result = sparse_matrix_expo(matrix, 10**7)
    
    # Sum the first row elements and apply modulo
    first_row = result[0, :].toarray()[0]
    ans = sum(first_row) % MOD
    
    print(f"Final answer: {ans}")

if __name__ == "__main__":
    main()