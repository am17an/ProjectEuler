import math

def sieve_squarefree(N):
    # Create a boolean list to mark square-free numbers
    is_squarefree = [True] * (N + 1)
    is_squarefree[0] = is_squarefree[1] = True  # 1 is considered square-free
    
    # Mark non-square-free numbers (those divisible by any p^2)
    for i in range(2, int(math.sqrt(N)) + 1):
        square = i * i
        for j in range(square, N + 1, square):
            is_squarefree[j] = False
    
    # Count the number of square-free numbers
    print(is_squarefree)
    return sum(is_squarefree[1:])

# Example usage:
N = 4
print(f"Number of square-free numbers <= {N}: {sieve_squarefree(N)}")