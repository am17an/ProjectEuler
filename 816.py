import math
import numpy as np
from scipy.spatial import cKDTree

def generate_points(n):
    """Generate n points using the specified random number generator."""
    s = [290797]
    points = []

    for i in range(2*n + 1):
        s.append((s[-1] * s[-1]) % 50515093)

    for i in range(n):
        points.append((s[2*i], s[2*i+1]))
    return points

def min_distance_kdtree(points):
    """Find the minimum distance between any two points using a KD-tree.
    This is much more efficient than the brute force approach."""
    
    # Convert points to numpy array for KD-tree
    points_array = np.array(points)
    
    # Build KD-tree
    tree = cKDTree(points_array)
    
    # For each point, find distance to its nearest neighbor
    # k=2 because the nearest point to itself (with distance 0) is itself
    distances, _ = tree.query(points_array, k=2)
    
    # The second column contains distances to the nearest different point
    min_dist = np.min(distances[:, 1])
    
    return min_dist

def verify_with_example():
    """Verify with the given example d(14) = 546446.466846479"""
    points = generate_points(14)
    
    # Use brute force for verification
    min_dist_brute = float('inf')
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            dist = math.sqrt((points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2)
            min_dist_brute = min(min_dist_brute, dist)
    
    # Use KD-tree approach
    min_dist_kdtree = min_distance_kdtree(points)
    
    print(f"Verification brute force: d(14) = {min_dist_brute}")
    print(f"Verification KD-tree: d(14) = {min_dist_kdtree}")
    print(f"Expected: 546446.466846479")
    
    # Check both results
    brute_force_ok = abs(min_dist_brute - 546446.466846479) < 1e-5
    kdtree_ok = abs(min_dist_kdtree - 546446.466846479) < 1e-5
    
    print(f"Brute force verification: {'✓' if brute_force_ok else '✗'}")
    print(f"KD-tree verification: {'✓' if kdtree_ok else '✗'}")
    
    return brute_force_ok and kdtree_ok

def main():
    print("Verifying algorithm with the example...")
    if verify_with_example():
        print("\nVerification successful! Proceeding with full calculation.")
        
        # Since we discovered the sequence has a cycle of length 6,308,948
        # and 2,000,000 < cycle length, we can use the KD-tree directly
        
        print("\nGenerating 2,000,000 points...")
        points = generate_points(2000000)
        
        print("Calculating minimum distance using KD-tree...")
        min_dist = min_distance_kdtree(points)
        
        # Format the answer to 9 decimal places
        formatted_answer = f"{min_dist:.9f}"
        print(f"\nAnswer: d(2000000) = {formatted_answer}")
    else:
        print("Verification failed. Please check the algorithm.")

if __name__ == "__main__":
    main()