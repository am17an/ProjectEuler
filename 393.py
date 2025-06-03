from itertools import product
from collections import defaultdict

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

def get_edge(pos1, pos2):
    """Get a canonical representation of the edge between two positions"""
    return tuple(sorted([pos1, pos2]))

def backtrack_optimized(current_row, n, occupied_positions, used_edges, row_assignments):
    """
    Optimized backtracking that processes ants row by row
    
    Args:
        current_row: Current row being processed (0 to n-1)
        n: Grid size
        occupied_positions: Set of positions already occupied by moved ants
        used_edges: Set of edges already used by moved ants
        row_assignments: List of lists, where row_assignments[i] contains the destination
                        positions for all ants that were originally in row i
    
    Returns:
        Number of valid configurations from this state
    """
    # Base case: all rows have been processed
    if current_row == n:
        return 1
    
    # Process all ants in the current row
    return backtrack_row_ants(current_row, 0, n, occupied_positions, used_edges, row_assignments, [])

def backtrack_row_ants(row, col, n, occupied_positions, used_edges, row_assignments, current_row_moves):
    """
    Backtrack through all ants in a specific row
    
    Args:
        row: Current row being processed
        col: Current column in the row being processed
        n: Grid size
        occupied_positions: Set of occupied destination positions
        used_edges: Set of used edges
        row_assignments: Previous row assignments
        current_row_moves: Current assignments for ants in this row
    
    Returns:
        Number of valid configurations
    """
    # If we've processed all columns in this row, move to next row
    if col == n:
        # Add current row moves to row_assignments
        new_row_assignments = row_assignments + [current_row_moves[:]]
        return backtrack_optimized(row + 1, n, occupied_positions, used_edges, new_row_assignments)
    
    # Get current ant's position
    start_pos = (row, col)
    
    # Get possible moves for this ant
    neighbors = get_neighbors(row, col, n)
    
    valid_configs = 0
    
    # Try each possible move for this ant
    for dest_i, dest_j in neighbors:
        dest_pos = (dest_i, dest_j)
        edge = get_edge(start_pos, dest_pos)
        
        # Check if this move is valid
        if dest_pos not in occupied_positions and edge not in used_edges:
            # Make the move
            occupied_positions.add(dest_pos)
            used_edges.add(edge)
            current_row_moves.append(dest_pos)
            
            # Continue with next ant in this row
            valid_configs += backtrack_row_ants(row, col + 1, n, occupied_positions, used_edges, row_assignments, current_row_moves)
            
            # Backtrack (undo the move)
            occupied_positions.remove(dest_pos)
            used_edges.remove(edge)
            current_row_moves.pop()
    
    return valid_configs

def f(n):
    """Compute f(n) - number of valid ant movement configurations"""
    if n == 1:
        return 0  # Single ant has no adjacent squares to move to
    
    occupied_positions = set()
    used_edges = set()
    row_assignments = []
    
    print(f"Computing f({n}) using optimized row-by-row backtracking...")
    result = backtrack_optimized(0, n, occupied_positions, used_edges, row_assignments)
    return result

def main():
    """Test the function for small values of n"""
    print("Computing f(n) for small values using backtracking:")
    
    for n in range(1, 7):
        result = f(n)
        print(f"f({n}) = {result}")
    
    # Verify the given value
    print(f"\nVerification: f(4) should be 88")

if __name__ == "__main__":
    main()
