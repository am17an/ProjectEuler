def generate_triangular_grid(n):
   """Generate list of triangles and their neighbors for n rows"""
   triangles = []
   neighbors = {}
   
   # Generate all triangles
   triangle_id = 0
   id_map = {}
   
   for row in range(n):
       for col in range(2 * row + 1):
           triangles.append((row, col))
           id_map[(row, col)] = triangle_id
           neighbors[triangle_id] = []
           triangle_id += 1
   
   # Find neighbors for each triangle
   for row in range(n):
       for col in range(2 * row + 1):
           current_id = id_map[(row, col)]
           
           # Check if triangle points up (even col) or down (odd col)
           points_up = (col % 2 == 1)
           
           # Add left and right neighbors for all triangles
           adjacent_positions = [
               (row, col - 1),  # left
               (row, col + 1),  # right
           ]
           
           # Add third neighbor based on orientation
           if points_up:
               # Upward triangles have a neighbor above
               adjacent_positions.append((row - 1, col - 1))
           else:
               # Downward triangles have a neighbor below
               adjacent_positions.append((row + 1, col + 1))
           
           for adj_row, adj_col in adjacent_positions:
               if (adj_row, adj_col) in id_map:
                   if 0 <= adj_row < n and 0 <= adj_col < 2 * adj_row + 1:
                       neighbors[current_id].append(id_map[(adj_row, adj_col)])
   
   return len(triangles), neighbors

def count_colorings_backtrack(num_triangles, neighbors, num_colors=3):
    """Efficiently count valid colorings using backtracking"""
    coloring = [-1] * num_triangles
    
    def is_valid(triangle, color):
        """Check if assigning color to triangle is valid"""
        for neighbor in neighbors[triangle]:
            if coloring[neighbor] == color:
                return False
        return True
    
    def backtrack(triangle):
        """Recursively try coloring triangles"""
        if triangle == num_triangles:
            print(coloring)
            return 1
        
        count = 0
        for color in range(num_colors):
            if is_valid(triangle, color):
                coloring[triangle] = color
                count += backtrack(triangle + 1)
                coloring[triangle] = -1
        
        return count
    
    return backtrack(0)

# Calculate for n = 1 to 5
for n in range(3, 5):
   num_triangles, neighbors = generate_triangular_grid(n)
   print(neighbors)
   valid_colorings = count_colorings_backtrack(num_triangles, neighbors)
   print(f"n={n}: {num_triangles} triangles, {valid_colorings} valid 3-colorings")