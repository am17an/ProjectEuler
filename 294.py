import numpy as np
from typing import List

class NumberCounter:
    def __init__(self, target_sum=23, divisor=23):
        self.target_sum = target_sum
        self.divisor = divisor
        self.mod = divisor
        self.max_sum = target_sum
        
        # Build the augmented transition matrix that also tracks cumulative count
        self.transition_matrix = self._build_augmented_transition_matrix()
        
    def _build_augmented_transition_matrix(self):
        """
        Build an augmented transition matrix that not only transitions between states
        but also tracks the cumulative count.
        
        The matrix has one extra row and column to track the cumulative sum.
        """
        # The state space is (remainder, digit_sum) + one extra state for accumulation
        matrix_size = self.mod * (self.max_sum + 1) + 1
        
        # Use dtype=object to use Python's arbitrary precision integers
        matrix = np.zeros((matrix_size, matrix_size), dtype=object)
        
        # For each current state (r, s)
        for r in range(self.mod):
            for s in range(self.max_sum + 1):
                curr_state_idx = r * (self.max_sum + 1) + s
                
                # Try adding each possible digit (0-9)
                for d in range(10):
                    # Check if adding this digit keeps sum ≤ target
                    if s + d <= self.max_sum:
                        # Calculate new state after adding digit d
                        new_r = (10 * r + d) % self.mod
                        new_s = s + d
                        new_state_idx = new_r * (self.max_sum + 1) + new_s
                        
                        # Add this transition to the matrix
                        matrix[new_state_idx, curr_state_idx] = int(matrix[new_state_idx, curr_state_idx]) + 1
                        
                        # If this transition creates a number with our target properties
                        # (remainder 0, digit sum = target), add it to the accumulator state
                        if new_r == 0 and new_s == self.target_sum:
                            # The last row is our accumulator
                            accumulator_idx = matrix_size - 1
                            matrix[accumulator_idx, curr_state_idx] = int(matrix[accumulator_idx, curr_state_idx]) + 1
        
        # Make the accumulator state preserve its value through transitions
        accumulator_idx = matrix_size - 1
        matrix[accumulator_idx, accumulator_idx] = 1
        
        return matrix
        
    def count_cumulative_sum_with_tracking(self, max_digits: int) -> List[int]:
        """
        Compute cumulative sum using the augmented transition matrix that
        directly tracks the sum in its state.
        """
        # Set up initial vector for leading digit (1-9)
        matrix_size = self.mod * (self.max_sum + 1) + 1
        initial_vector = np.zeros(matrix_size, dtype=object)
        
        for d in range(1, 10):
            r = d % self.mod
            s = d
            if s <= self.max_sum:
                state_idx = r * (self.max_sum + 1) + s
                initial_vector[state_idx] = int(initial_vector[state_idx]) + 1
        
        # The accumulator starts at 0
        accumulator_idx = matrix_size - 1
        initial_vector[accumulator_idx] = 0
        
        result = []
        current_vector = initial_vector.copy()
        
        # Apply the transition matrix for each digit length
        for d in range(1, max_digits + 1):
            # For the first digit, we need to count directly
            if d == 1:
                # Count how many 1-digit numbers meet our criteria
                target_state_idx = 0 * (self.max_sum + 1) + self.target_sum
                initial_count = int(current_vector[target_state_idx])
                
                # Add this to the accumulator
                current_vector[accumulator_idx] = int(current_vector[accumulator_idx]) + initial_count
            else:
                # Apply the transition matrix which automatically updates the accumulator
                current_vector = np.matmul(self.transition_matrix, current_vector)
            
            # Read the cumulative count from the accumulator state
            result.append(int(current_vector[accumulator_idx]))
        
        return result
        
    # For standard implementation comparison
    def count_cumulative_sum_efficient(self, max_digits: int) -> List[int]:
        """
        Original implementation that avoids recomputing matrices
        for each digit count, but uses a separate accumulator.
        """
        result = []
        total_count = 0
        
        # Set up initial vector for leading digit (1-9)
        matrix_size = self.mod * (self.max_sum + 1)
        initial_vector = np.zeros(matrix_size, dtype=object)
        
        for d in range(1, 10):
            r = d % self.mod
            s = d
            if s <= self.max_sum:
                state_idx = r * (self.max_sum + 1) + s
                initial_vector[state_idx] = int(initial_vector[state_idx]) + 1
        
        current_vector = initial_vector.copy()
        
        # Extract count for state [0, target_sum] for 1 digit
        target_state_idx = 0 * (self.max_sum + 1) + self.target_sum
        total_count += int(current_vector[target_state_idx])
        result.append(total_count)
        
        # Create standard transition matrix (without accumulator)
        std_matrix = np.zeros((matrix_size, matrix_size), dtype=object)
        for r in range(self.mod):
            for s in range(self.max_sum + 1):
                curr_state_idx = r * (self.max_sum + 1) + s
                for d in range(10):
                    if s + d <= self.max_sum:
                        new_r = (10 * r + d) % self.mod
                        new_s = s + d
                        new_state_idx = new_r * (self.max_sum + 1) + new_s
                        std_matrix[new_state_idx, curr_state_idx] = int(std_matrix[new_state_idx, curr_state_idx]) + 1
                        
        # For each additional digit
        for d in range(2, max_digits + 1):
            # Multiply by transition matrix
            current_vector = np.matmul(std_matrix, current_vector)
            
            # Add count to total
            total_count += int(current_vector[target_state_idx])
            result.append(total_count)
        
        return result
    
    # Matrix exponentiation with arbitrary precision
    def matrix_power(self, matrix, power, modulus=None):
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
        half = self.matrix_power(matrix, power // 2, modulus)
        
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
        
    def count_cumulative_sum_large(self, max_digits: int, modulus=None) -> int:
        """
        Compute the cumulative sum for extremely large max_digits using
        matrix exponentiation with arbitrary precision integers.
        """
        if max_digits <= 0:
            return 0
            
        # Initialize with object dtype for arbitrary precision 
        matrix_size = self.mod * (self.max_sum + 1) + 1
        initial_vector = np.zeros(matrix_size, dtype=object)
        
        # Set up initial vector as before
        for d in range(1, 10):
            r = d % self.mod
            s = d
            if s <= self.max_sum:
                state_idx = r * (self.max_sum + 1) + s
                initial_vector[state_idx] = int(initial_vector[state_idx]) + 1
        
        # The accumulator starts at 0
        accumulator_idx = matrix_size - 1
        initial_vector[accumulator_idx] = 0
        
        # For the first digit, count directly
        target_state_idx = 0 * (self.max_sum + 1) + self.target_sum
        initial_count = int(initial_vector[target_state_idx])
        initial_vector[accumulator_idx] = int(initial_vector[accumulator_idx]) + initial_count
        
        # For D=1, return the accumulator value
        if max_digits == 1:
            return int(initial_vector[accumulator_idx])
        
        # For larger D, use matrix exponentiation
        # We need to compute M^(max_digits-1) * v
        if modulus:
            # Make a copy of the matrix with modular values
            mod_matrix = self.transition_matrix.copy()
            for i in range(matrix_size):
                for j in range(matrix_size):
                    if mod_matrix[i, j] != 0:
                        mod_matrix[i, j] = int(mod_matrix[i, j]) % modulus
            
            # Compute the power using binary exponentiation
            powered_matrix = self.matrix_power(mod_matrix, max_digits-1, modulus)
            
            # Apply to initial vector
            result_vector = np.zeros_like(initial_vector)
            for i in range(matrix_size):
                for j in range(matrix_size):
                    if powered_matrix[i, j] != 0 and initial_vector[j] != 0:
                        value = (int(powered_matrix[i, j]) * int(initial_vector[j])) % modulus
                        result_vector[i] = (int(result_vector[i]) + value) % modulus
        else:
            # Use binary exponentiation with arbitrary precision
            powered_matrix = self.matrix_power(self.transition_matrix, max_digits-1)
            
            # Apply to initial vector using manual multiplication for better precision
            result_vector = np.zeros_like(initial_vector)
            for i in range(matrix_size):
                for j in range(matrix_size):
                    if powered_matrix[i, j] != 0 and initial_vector[j] != 0:
                        result_vector[i] = int(result_vector[i]) + int(powered_matrix[i, j]) * int(initial_vector[j])
        
        # Return the value from the accumulator state
        return int(result_vector[accumulator_idx])

# Example usage
def main():
    # Initialize counter
    counter = NumberCounter(target_sum=23, divisor=23)
    
    # Compute cumulative counts for 1 to 10 digits
    max_digits = 10
    cumulative_counts = counter.count_cumulative_sum_with_tracking(max_digits)
    
    print(f"Cumulative counts for 1 to {max_digits} digits:")
    for d, count in enumerate(cumulative_counts, 1):
        print(f"{d} digits: {count}")
    
    # Test the original method and compare
    original_counts = counter.count_cumulative_sum_efficient(max_digits)
    print("\nComparing with original method:")
    print("Digit | With Tracking | Original | Match?")
    print("----------------------------------------")
    for d in range(max_digits):
        digit = d + 1
        match = "Yes" if cumulative_counts[d] == original_counts[d] else "No"
        print(f"{digit:5d} | {cumulative_counts[d]:13d} | {original_counts[d]:8d} | {match}")
    
    # Test for a larger value
    large_D = 100
    modulus = 10**9 
    print(f"\nCumulative count for {large_D} digits:")
    large_count = counter.count_cumulative_sum_large(large_D)
    print(large_count%modulus)
    
    # Test with extremely large value and modular arithmetic
    extreme_D = 11**12
    print(f"\nCumulative count for {extreme_D} digits (mod {modulus}):")
    extreme_count = counter.count_cumulative_sum_large(extreme_D, modulus)
    print(extreme_count)

if __name__ == "__main__":
    main()