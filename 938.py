import time
import math

def P(R, B):
    """
    Calculate P(R,B) using bottom-up DP, storing only the last 3 rows.
    P(R,B) is the probability that all remaining cards are black when the game ends.
    """
    # Base cases
    if R == 0 and B > 0:
        return 1.0  # All cards are black
    if B == 0:
        return 0.0  # All cards are red
    
    # Use DP with limited memory (only 3 rows)
    # dp[i % 3] will represent P(i, :)
    dp = [{} for _ in range(3)]
    
    # Fill base cases
    for b in range(B + 1):
        dp[0][b] = 1.0 if b > 0 else 0.0  # P(0,b) = 1.0 if b > 0 else 0.0
    
    # First row: P(1,b)
    for b in range(B + 1):
        if b == 0:
            dp[1][b] = 0.0
        elif b == 1:
            dp[1][b] = 0.5
        elif b == 2:
            dp[1][b] = 0.6
        else:
            # Calculate P(1,b) using the recurrence
            N = 1 + b
            p_black_black = (b * (b - 1)) / (N * (N - 1))
            p_red_black = (2 * 1 * b) / (N * (N - 1))
            
            dp[1][b] = (p_red_black * dp[1][b-1]) / (1.0 - p_black_black)
    
    # Fill DP table row by row, keeping only last 3 rows
    for r in range(2, R + 1):
        for b in range(B + 1):
            if b == 0:
                dp[r % 3][b] = 0.0
            else:
                N = r + b
                
                # Probability of drawing two red cards and discarding them
                p_red_red = (r * (r - 1)) / (N * (N - 1))
                
                # Probability of drawing two black cards and putting them back
                p_black_black = (b * (b - 1)) / (N * (N - 1))
                
                # Probability of drawing one of each color
                p_red_black = (2 * r * b) / (N * (N - 1))
                
                # DP recurrence using values from at most 2 rows back
                numerator = p_red_red * dp[(r-2) % 3][b] + p_red_black * dp[r % 3][b-1]
                denominator = 1.0 - p_black_black
                dp[r % 3][b] = numerator / denominator
    
    return dp[R % 3][B]

# Verify the given examples
print(f"P(2,2) = {P(2,2)}")  # Should be 0.4666666667
print(f"P(10,9) = {P(10,9)}")  # Should be 0.4118903397
print(f"P(34,25) = {P(34,25)}")  # Should be 0.3665688069
print(f"P(2,1) = {P(2,1)}")  # Should be 0.3665688069
print(f"P(4,2) = {P(4,2)}")  # Should be 0.3665688069

for i in range(1, 11):
    print(f"P(10, {i}) = {P(10, i)}")

# For the large input
print("\nComputing P(24690, 12345)...")
start_time = time.time()
result = P(24690, 12345)
end_time = time.time()
print(f"P(24690, 12345) = {result}")
print(f"Computation time: {end_time - start_time:.2f} seconds")