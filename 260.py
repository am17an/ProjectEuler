def is_winning(x, y, z, memo):
    """
    Determine if a configuration (x, y, z) is winning for the current player.
    A configuration is winning if there exists at least one move that leads to a losing position for the opponent.
    A configuration is losing if all possible moves lead to winning positions for the opponent.
    """
    # Sort to ensure canonical form
    state = tuple(sorted([x, y, z]))
    
    if state in memo:
        return memo[state]
    
    # Base case: if all piles are empty, the current player has already lost
    if state == (0, 0, 0):
        memo[state] = False
        return False
    
    x, y, z = state
    
    # Try all possible moves
    # Move 1: Remove N stones from a single pile
    for pile_idx in range(3):
        piles = [x, y, z]
        for n in range(1, piles[pile_idx] + 1):
            new_piles = piles[:]
            new_piles[pile_idx] -= n
            if not is_winning(new_piles[0], new_piles[1], new_piles[2], memo):
                memo[state] = True
                return True
    
    # Move 2: Remove N stones from each of two piles
    for i in range(3):
        for j in range(i + 1, 3):
            piles = [x, y, z]
            max_n = min(piles[i], piles[j])
            for n in range(1, max_n + 1):
                new_piles = piles[:]
                new_piles[i] -= n
                new_piles[j] -= n
                if not is_winning(new_piles[0], new_piles[1], new_piles[2], memo):
                    memo[state] = True
                    return True
    
    # Move 3: Remove N stones from all three piles
    max_n = min(x, y, z)
    for n in range(1, max_n + 1):
        if not is_winning(x - n, y - n, z - n, memo):
            memo[state] = True
            return True
    
    # If no move leads to a losing position for the opponent, this is a losing position
    memo[state] = False
    return False

def find_losing_configurations(max_val):
    """Find all losing configurations where x <= y <= z <= max_val"""
    memo = {}
    losing_configs = []
    
    print(f"Finding losing configurations for max_val = {max_val}")
    total_configs = (max_val + 1) * (max_val + 2) * (max_val + 3) // 6
    processed = 0
    
    for x in range(max_val + 1):
        if x % 50 == 0:
            print(f"Progress: x = {x}/{max_val} ({100*processed/total_configs:.1f}%)")
        for y in range(x, max_val + 1):
            for z in range(y, max_val + 1):
                processed += 1
                if not is_winning(x, y, z, memo):
                    losing_configs.append((x, y, z))
    
    return losing_configs

# Test with small values first to verify our logic
print("Testing with small values (max = 10):")
small_losing = find_losing_configurations(10)
print(f"Found {len(small_losing)} losing configurations:")
for config in small_losing:
    print(config)

print(f"\nSum for max=10: {sum(sum(config) for config in small_losing)}")

# Verify the given example for max=100
print("\nTesting with max=100:")
losing_100 = find_losing_configurations(100)
sum_100 = sum(sum(config) for config in losing_100)
print(f"Number of losing configurations: {len(losing_100)}")
print(f"Sum for max=100: {sum_100}")
print(f"Expected: 173895, Got: {sum_100}, Match: {sum_100 == 173895}")

# Show some examples of losing and winning configurations
print("\nFirst 20 losing configurations:")
for i, config in enumerate(losing_100):
    print(f"{config}: sum = {sum(config)}")

print("\nSome winning configurations for comparison:")
memo = {}
winning_examples = []
for x in range(11):
    for y in range(x, 11):
        for z in range(y, 11):
            if is_winning(x, y, z, memo):
                winning_examples.append((x, y, z))
                if len(winning_examples) >= 10:
                    break
        if len(winning_examples) >= 10:
            break
    if len(winning_examples) >= 10:
        break

for config in winning_examples:
    print(f"{config}: sum = {sum(config)}")

# Now solve the actual problem for max=1000
print("\n" + "="*50)
print("SOLVING THE ACTUAL PROBLEM (max = 1000)")
print("This will take a significant amount of time...")
print("="*50)

losing_1000 = find_losing_configurations(1000)
sum_1000 = sum(sum(config) for config in losing_1000)
print(f"\nFINAL ANSWER:")
print(f"Number of losing configurations with max=1000: {len(losing_1000)}")
print(f"Sum of all (x_i + y_i + z_i) for max=1000: {sum_1000}")

# Save some sample losing configurations for analysis
print(f"\nFirst 50 losing configurations for max=1000:")
for i, config in enumerate(losing_1000[:50]):
    print(f"{config}: sum = {sum(config)}")

print(f"\nLast 10 losing configurations for max=1000:")
for config in losing_1000[-10:]:
    print(f"{config}: sum = {sum(config)}")
