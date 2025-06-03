from collections import defaultdict
import time

def get_neighbors(i, j, n):
    """Get valid adjacent positions for position (i, j) in an n×n grid"""
    neighbors = []
    # Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < n:
            neighbors.append((ni, nj))
    
    return neighbors

def pos_to_bit(i, j, n):
    """Convert (i, j) position to bit index"""
    return i * n + j

def bit_to_pos(bit, n):
    """Convert bit index to (i, j) position"""
    return (bit // n, bit % n)

def f_bitmask_dp(n):
    """
    Solve using bitmask DP
    
    State: (ant_index, occupied_mask, used_edges_signature)
    - ant_index: which ant we're currently placing (0 to n²-1)
    - occupied_mask: bitmask of which destination squares are occupied
    - used_edges_signature: some representation of used edges
    
    The challenge is representing used edges efficiently...
    """
    if n == 1:
        return 0
    
    total_ants = n * n
    
    # For small n, we can represent used edges as a set in the state
    # But for bitmask DP, we need a more compact representation
    
    # Let's try a different approach: process ants in order and track states
    memo = {}
    
    def dp(ant_idx, occupied_mask, used_edges_tuple):
        """
        DP function
        ant_idx: current ant being processed (0 to total_ants-1)
        occupied_mask: bitmask of occupied destination positions
        used_edges_tuple: tuple of used edges (for memoization)
        """
        if ant_idx == total_ants:
            return 1
        
        state = (ant_idx, occupied_mask, used_edges_tuple)
        if state in memo:
            return memo[state]
        
        # Get current ant's position
        start_i, start_j = ant_idx // n, ant_idx % n
        start_bit = pos_to_bit(start_i, start_j, n)
        
        # Get possible moves for this ant
        neighbors = get_neighbors(start_i, start_j, n)
        
        result = 0
        
        for dest_i, dest_j in neighbors:
            dest_bit = pos_to_bit(dest_i, dest_j, n)
            
            # Check if destination is already occupied
            if occupied_mask & (1 << dest_bit):
                continue
            
            # Create edge representation (canonical form)
            edge = tuple(sorted([(start_i, start_j), (dest_i, dest_j)]))
            
            # Check if edge is already used
            if edge in used_edges_tuple:
                continue
            
            # Make the move
            new_occupied_mask = occupied_mask | (1 << dest_bit)
            new_used_edges = used_edges_tuple + (edge,)
            
            result += dp(ant_idx + 1, new_occupied_mask, new_used_edges)
        
        memo[state] = result
        return result
    
    return dp(0, 0, ())

def f_bitmask_optimized(n):
    """
    More optimized bitmask DP approach
    
    Key insight: instead of tracking used edges explicitly, we can use
    the fact that if we process ants in a specific order, we can avoid
    some edge conflicts naturally.
    """
    if n == 1:
        return 0
    
    total_ants = n * n
    
    # Create adjacency list for each position
    adj = {}
    for i in range(n):
        for j in range(n):
            adj[(i, j)] = get_neighbors(i, j, n)
    
    # DP with bitmask for occupied positions
    # We'll track used edges separately but more efficiently
    
    def solve():
        # dp[mask] = number of ways to reach this occupied configuration
        # But we need to also track which ant is at which position...
        
        # Alternative: dp[ant_idx][mask] = ways to place first ant_idx ants
        # with destinations given by mask
        
        dp = defaultdict(int)
        dp[(0, 0)] = 1  # (ant_index, occupied_mask)
        
        for ant_idx in range(total_ants):
            new_dp = defaultdict(int)
            start_i, start_j = ant_idx // n, ant_idx % n
            
            for (curr_ant_idx, occupied_mask), ways in dp.items():
                if curr_ant_idx != ant_idx:
                    continue
                
                # Try each possible destination for current ant
                for dest_i, dest_j in adj[(start_i, start_j)]:
                    dest_bit = pos_to_bit(dest_i, dest_j, n)
                    
                    # Check if destination is available
                    if occupied_mask & (1 << dest_bit):
                        continue
                    
                    # Check edge conflicts (this is the tricky part)
                    # For now, let's use a simpler approach
                    
                    new_mask = occupied_mask | (1 << dest_bit)
                    new_dp[(ant_idx + 1, new_mask)] += ways
            
            dp = new_dp
        
        # Sum all ways where all ants are placed
        return sum(ways for (ant_idx, mask), ways in dp.items() 
                  if ant_idx == total_ants)
    
    return solve()

def f_bitmask_with_edge_tracking(n):
    """
    Bitmask DP with proper edge conflict tracking
    
    This is more complex but handles the edge constraint correctly
    """
    if n == 1:
        return 0
    
    total_ants = n * n
    
    # Pre-compute all possible edges
    all_edges = set()
    edge_to_id = {}
    for i in range(n):
        for j in range(n):
            for ni, nj in get_neighbors(i, j, n):
                edge = tuple(sorted([(i, j), (ni, nj)]))
                if edge not in edge_to_id:
                    edge_to_id[edge] = len(all_edges)
                    all_edges.add(edge)
    
    print(f"Total edges: {len(all_edges)}")
    
    # If too many edges, this approach becomes impractical
    if len(all_edges) > 20:  # 2^20 = ~1M states
        print("Too many edges for bitmask DP")
        return None
    
    memo = {}
    
    def dp(ant_idx, occupied_mask, used_edges_mask):
        if ant_idx == total_ants:
            return 1
        
        state = (ant_idx, occupied_mask, used_edges_mask)
        if state in memo:
            return memo[state]
        
        start_i, start_j = ant_idx // n, ant_idx % n
        result = 0
        
        for dest_i, dest_j in get_neighbors(start_i, start_j, n):
            dest_bit = pos_to_bit(dest_i, dest_j, n)
            
            # Check if destination is occupied
            if occupied_mask & (1 << dest_bit):
                continue
            
            # Check if edge is used
            edge = tuple(sorted([(start_i, start_j), (dest_i, dest_j)]))
            edge_id = edge_to_id[edge]
            
            if used_edges_mask & (1 << edge_id):
                continue
            
            # Make the move
            new_occupied_mask = occupied_mask | (1 << dest_bit)
            new_used_edges_mask = used_edges_mask | (1 << edge_id)
            
            result += dp(ant_idx + 1, new_occupied_mask, new_used_edges_mask)
        
        memo[state] = result
        return result
    
    return dp(0, 0, 0)

def main():
    print("Testing bitmask DP approaches:")
    
    for n in range(2, 5):
        print(f"\n=== n = {n} ===")
        
        # Method 1: Simple DP with tuple for edges (slow but correct)
        start_time = time.time()
        result1 = f_bitmask_dp(n)
        time1 = time.time() - start_time
        print(f"Bitmask DP (tuple edges): f({n}) = {result1} (Time: {time1:.3f}s)")
        
        # Method 2: Optimized bitmask DP with edge bitmask (if feasible)
        start_time = time.time()
        result2 = f_bitmask_with_edge_tracking(n)
        time2 = time.time() - start_time
        if result2 is not None:
            print(f"Bitmask DP (edge bitmask): f({n}) = {result2} (Time: {time2:.3f}s)")
            
            if result1 == result2:
                print("✓ Results match!")
            else:
                print("✗ Results don't match!")

if __name__ == "__main__":
    main() 