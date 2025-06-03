import sys
from functools import lru_cache

# Increase recursion limit for deep memoization
sys.setrecursionlimit(10000)

@lru_cache(maxsize=None)
def is_winning(x, y, z):
    """
    Determine if a configuration (x, y, z) is winning for the current player.
    Using lru_cache for automatic memoization.
    """
    # Sort to ensure canonical form
    x, y, z = sorted([x, y, z])
    
    # Base case: if all piles are empty, the current player has already lost
    if x == 0 and y == 0 and z == 0:
        return False
    
    # Try all possible moves
    # Move 1: Remove N stones from a single pile
    # Remove from pile with x stones
    for n in range(1, x + 1):
        if not is_winning(x - n, y, z):
            return True
    
    # Remove from pile with y stones (if y > x)
    if y > x:
        for n in range(1, y + 1):
            if not is_winning(x, y - n, z):
                return True
    
    # Remove from pile with z stones (if z > y)
    if z > y:
        for n in range(1, z + 1):
            if not is_winning(x, y, z - n):
                return True
    
    # Move 2: Remove N stones from each of two piles
    # Remove from x and y piles
    if x > 0 and y > 0:
        for n in range(1, min(x, y) + 1):
            if not is_winning(x - n, y - n, z):
                return True
    
    # Remove from x and z piles
    if x > 0 and z > 0:
        for n in range(1, min(x, z) + 1):
            if not is_winning(x - n, y, z - n):
                return True
    
    # Remove from y and z piles
    if y > 0 and z > 0:
        for n in range(1, min(y, z) + 1):
            if not is_winning(x, y - n, z - n):
                return True
    
    # Move 3: Remove N stones from all three piles
    if x > 0 and y > 0 and z > 0:
        for n in range(1, min(x, y, z) + 1):
            if not is_winning(x - n, y - n, z - n):
                return True
    
    # If no move leads to a losing position for the opponent, this is a losing position
    return False

def find_losing_configurations_optimized(max_val):
    """Find all losing configurations where x <= y <= z <= max_val"""
    losing_configs = []
    total_configs = (max_val + 1) * (max_val + 2) * (max_val + 3) // 6
    processed = 0
    
    print(f"Finding losing configurations for max_val = {max_val}")
    print(f"Total configurations to check: {total_configs}")
    
    for x in range(max_val + 1):
        if x % 100 == 0:
            print(f"Progress: x = {x}/{max_val} ({100*processed/total_configs:.2f}%) - Found {len(losing_configs)} losing configs so far")
        
        for y in range(x, max_val + 1):
            for z in range(y, max_val + 1):
                processed += 1
                if not is_winning(x, y, z):
                    losing_configs.append((x, y, z))
    
    return losing_configs

# Test with smaller values first
print("Testing with max=50:")
losing_50 = find_losing_configurations_optimized(50)
sum_50 = sum(sum(config) for config in losing_50)
print(f"Number of losing configurations: {len(losing_50)}")
print(f"Sum for max=50: {sum_50}")

print("\nTesting with max=100:")
losing_100 = find_losing_configurations_optimized(100)
sum_100 = sum(sum(config) for config in losing_100)
print(f"Number of losing configurations: {len(losing_100)}")
print(f"Sum for max=100: {sum_100}")
print(f"Expected: 173895, Match: {sum_100 == 173895}")

# Clear cache before the big computation
is_winning.cache_clear()

print("\n" + "="*60)
print("SOLVING THE ACTUAL PROBLEM (max = 1000)")
print("This will take a very long time with brute force...")
print("="*60)

losing_1000 = find_losing_configurations_optimized(1000)
sum_1000 = sum(sum(config) for config in losing_1000)

print(f"\nFINAL ANSWER:")
print(f"Number of losing configurations with max=1000: {len(losing_1000)}")
print(f"Sum of all (x_i + y_i + z_i) for max=1000: {sum_1000}")

# Show cache statistics
print(f"\nCache info: {is_winning.cache_info()}")

# Save results to file
with open('losing_configs_1000.txt', 'w') as f:
    f.write(f"Number of losing configurations: {len(losing_1000)}\n")
    f.write(f"Sum: {sum_1000}\n")
    f.write("Configurations:\n")
    for config in losing_1000:
        f.write(f"{config}\n")

print("Results saved to losing_configs_1000.txt") 