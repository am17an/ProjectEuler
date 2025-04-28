
import numpy as np
def create_transition_matrix():

    array = np.zeros((18, 18), dtype=object)

    for i in range(9):
        array[i][0] = 10

    for i in range(9, 18):
        array[i][0] = i - 9 + 1

    for i in range(0, 9):
        array[i][i+1] = 1

    for i in range(9, 18):
        array[i][9] = 1


    for i in range(9, 17):
        array[i][i+1] = 1
        
    return array


def create_transition_matrix2():
    array = np.zeros((20, 20), dtype=object)
    
    # F recurrence coefficients
    for i in range(10):  # 10 F states
        array[i][0] = 10
    
    # G recurrence coefficients
    for i in range(10, 20):  # 10 G states
        array[i][0] = i - 10 + 1  # k values from 1 to 10
    
    # F shift registers
    for i in range(0, 9):
        array[i][i+1] = 1
    
    # G contributions
    for i in range(10, 20):
        array[i][10] = 1  # Column 10 is G(0)
    
    # G shift registers
    for i in range(10, 19):
        array[i][i+1] = 1

    array[19][0] = 0
    array[19][10] = 0

    array[9][0] = 0
    
    return array
 
def create_initial_vector():
    array = np.zeros((1, 20), dtype=object)

    array[0][0] = 0
    array[0][10] = 1

    return array


def exponentiate(A, n, mod=10**9):
    """Compute A^n mod 'mod' using binary exponentiation."""
    # A is already a matrix
    A = A.astype(object)
    result = np.eye(A.shape[0], dtype=object)  # Identity matrix with same dimension as A
    
    while n > 0:
        if n % 2 == 1:
            result = np.mod(result @ A, mod)  # Corrected order
        A = np.mod(A @ A, mod)  # Square the matrix
        n = n // 2
        
    return result


B = create_transition_matrix2()  # 18×18 transition matrix
print(B)
initial_vector = create_initial_vector()  # 1×18 vector

# Calculate B^(13^i - 1)
total = 0
for i in range(1, 18):
    power = 13**i
    B_power = exponentiate(B, power)  # Exponentiate the transition matrix

    # Multiply initial vector by the exponentiated matrix
    result = initial_vector @ B_power  # 1×18 result
    
    print(f"i: {i}, ans: {result[0][0]}")
    total += result[0][0]
    total = total % 10**9

print(total)