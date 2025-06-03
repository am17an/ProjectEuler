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
    
    for x in range(max_val + 1):
        for y in range(x, max_val + 1):
            for z in range(y, max_val + 1):
                if not is_winning(x, y, z, memo):
                    losing_configs.append((x, y, z))
    
    return losing_configs

# Test the examples given in the problem
print("Testing specific examples from the problem:")
memo = {}

# Winning configurations mentioned
winning_examples = [(0,0,13), (0,11,11), (5,5,5)]
for config in winning_examples:
    result = is_winning(*config, memo)
    print(f"{config}: {'WINNING' if result else 'LOSING'} (expected: WINNING)")

# Losing configurations mentioned  
losing_examples = [(0,1,2), (1,3,3)]
for config in losing_examples:
    result = is_winning(*config, memo)
    print(f"{config}: {'WINNING' if result else 'LOSING'} (expected: LOSING)")

print("\nTesting with small values (max = 20):")
small_losing = find_losing_configurations(20)
print(f"Found {len(small_losing)} losing configurations")
print(f"Sum for max=20: {sum(sum(config) for config in small_losing)}")

print("\nFirst 30 losing configurations:")
for i, config in enumerate(small_losing[:30]):
    print(f"{config}: sum = {sum(config)}")

print("\nVerifying with max=100:")
losing_100 = find_losing_configurations(100)
sum_100 = sum(sum(config) for config in losing_100)
print(f"Number of losing configurations: {len(losing_100)}")
print(f"Sum for max=100: {sum_100}")
print(f"Expected: 173895, Got: {sum_100}, Match: {sum_100 == 173895}")

# Print sorted sums of losing configurations
sums = [sum(config) for config in losing_100]
sums.sort()
print(f"\nSorted sums of losing configurations (first 50):")
for i, s in enumerate(sums[:50]):
    print(f"{i+1}: {s}")

print(f"\nSorted sums of losing configurations (last 20):")
for i, s in enumerate(sums[-20:], len(sums)-19):
    print(f"{i}: {s}")

print(f"\nAll sorted sums:")
print(sums)

# Analyze patterns in losing configurations
print("\nAnalyzing patterns in losing configurations:")
patterns = {}
for x, y, z in losing_100:
    if x == 0:
        diff = z - y
        if diff not in patterns:
            patterns[diff] = []
        patterns[diff].append((x, y, z))

print("Patterns where x=0:")
for diff in sorted(patterns.keys())[:10]:
    print(f"z-y = {diff}: {patterns[diff][:5]}...")  # Show first 5 examples 