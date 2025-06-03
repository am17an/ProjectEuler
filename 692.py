from functools import cache

@cache
def can_win(heap, prev_take):
    """
    Check if the current player can win with optimal play
    heap: remaining pebbles
    prev_take: how many pebbles the previous player took
    """
    if heap == 0:
        return False  # Current player lost (no pebbles to take)
    
    max_take = min(heap, prev_take * 2 if prev_take > 0 else heap)
    
    # Try all possible moves
    for take in range(1, max_take + 1):
        # If opponent cannot win after our move, we win
        if not can_win(heap - take, take):
            return True
    
    return False  # No winning move found

@cache
def find_min_winning_move(heap):
    """
    Find the minimum number of pebbles Siegbert needs to take to win
    """
    # Siegbert can take between 1 and N pebbles on first move
    for take in range(1, heap + 1):
        # If Jo cannot win after Siegbert's move, Siegbert wins
        if not can_win(heap - take, take):
            return take
    
    return heap  # Default: take all pebbles

@cache
def H(n):
    """Calculate H(n) - the minimal amount for a heap of n pebbles"""
    return find_min_winning_move(n)

def G(n):
    """Calculate G(n) - the sum of H(k) for k from 1 to n"""
    return sum(H(k) for k in range(1, n + 1))

# Calculate H(n) for values from 1 to 100
for n in range(1, 101):
    print(f"H({n}) = {H(n)}, G{n}: {G(n)}") 