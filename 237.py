import numpy as np 


def matrix_power(matrix, power, modulus=None):
    """
    Compute matrix^power efficiently using binary exponentiation.
    Uses arbitrary precision integers to avoid overflow.
    """
    if power == 0:
        # Return identity matrix of same size as input
        identity = np.eye(matrix.shape[0], dtype=object)
        for i in range(matrix.shape[0]):
            identity[i, i] = int(1)  # Ensure it's a Python int
        return identity
    
    if power == 1:
        return matrix.copy()
        
    # Binary exponentiation
    half = matrix_power(matrix, power // 2, modulus)
    
    if power % 2 == 0:
        # power is even: result = half² 
        if modulus:
            result = np.matmul(half, half) % modulus
        else:
            result = np.matmul(half, half)
    else:
        # power is odd: result = half² * matrix
        if modulus:
            result = np.matmul(np.matmul(half, half) % modulus, matrix) % modulus
        else:
            result = np.matmul(np.matmul(half, half), matrix)
            
    return result

def make_matrix():
    matrix = np.zeros((4, 4), dtype=np.int64)

    matrix[:, 0] = [2, 2, -2, 1]
    matrix[:, 1] = [1, 0, 0, 0]
    matrix[:, 2] = [0, 1, 0, 0]
    matrix[:, 3] = [0, 0, 1, 0]

    return matrix

M = make_matrix()

initial = np.array([8, 4, 1, 1])

print((initial @ matrix_power(M, 10**12 - 4, 10**8))[0]%(10**8))