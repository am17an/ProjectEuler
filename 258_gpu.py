import torch
import numpy as np

# Define constants
SIZE = 2000
MOD = 20092010

def matrix_multiply_gpu(A, B):
    """Multiply two int32 matrices on GPU with modular arithmetic."""
    C = torch.matmul(A, B) % MOD
    return C

def matrix_expo_gpu(matrix, n):
    """Compute matrix^n using binary exponentiation on GPU."""
    # Start with identity matrix
    result = torch.eye(SIZE, dtype=torch.int32, device=matrix.device)
    power = matrix.clone()
    
    while n > 0:
        print(f"Remaining power: {n}")
        if n % 2 == 1:
            result = matrix_multiply_gpu(result, power)
        power = matrix_multiply_gpu(power, power)
        n //= 2
    
    return result

def main():
    # Check if CUDA is available
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("Using CUDA")
    else:
        device = torch.device("cpu")
        print("CUDA not available, using CPU")
    
    # Initialize the matrix on GPU with int32 type
    matrix = torch.zeros((SIZE, SIZE), dtype=torch.int32, device=device)
    
    # Set the first column according to the recurrence relation
    matrix[SIZE-1, 0] = 1
    matrix[SIZE-2, 0] = 1
    
    # Set the diagonal shift
    for row in range(SIZE-1):
        matrix[row, row+1] = 1
    
    # Compute matrix^20000
    result = matrix_expo_gpu(matrix, 20000)
    
    # Sum the first row elements and apply modulo
    ans = torch.sum(result[0, :]) % MOD
    
    print(f"Final answer: {ans.item()}")

if __name__ == "__main__":
    main()
