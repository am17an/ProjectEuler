from collections import defaultdict
import math
import time
import matplotlib.pyplot as plt
from bisect import insort_left, bisect_left
import heapq

def generate_points(n):
    """
    Generate n points according to the given formula:
    S_0 = 290797
    S_{n+1} = S_n^2 mod 50515093
    T_n = (S_n mod 2000) - 1000
    """
    points = []
    s = 290797
    
    for i in range(1, 2*n+1):
        s = (s**2) % 50515093
        t = (s % 2000) - 1000
        
        if i % 2 == 1:  # Odd index: T_{2k-1} (x-coordinate)
            x = t
        else:  # Even index: T_{2k} (y-coordinate)
            y = t
            points.append((x, y))
    
    return points

def is_multiple(a, b, epsilon=1e-9):
    """Check if a and b are scalar multiples of each other."""
    if abs(a[0]) < epsilon and abs(b[0]) < epsilon:
        return abs(a[1]) < epsilon or abs(b[1]) < epsilon
    if abs(a[0]) < epsilon or abs(b[0]) < epsilon:
        return False
    if abs(a[1]) < epsilon and abs(b[1]) < epsilon:
        return True
    if abs(a[1]) < epsilon or abs(b[1]) < epsilon:
        return False
    return abs(a[0]/b[0] - a[1]/b[1]) < epsilon

def line_intersection(line1, line2):
    """Calculate the intersection point of two lines in ax + by + c = 0 form."""
    a1, b1, c1 = line1
    a2, b2, c2 = line2
    
    det = a1 * b2 - a2 * b1
    if det == 0:  # Parallel lines
        return None
        
    x = (b1 * c2 - b2 * c1) / det
    y = (a2 * c1 - a1 * c2) / det
    return (x, y)

def solve_sweep_line(n):
    """Solve using a sweep-line algorithm for calculating intersections."""
    start_time = time.time()
    print(f"Generating {n} points...")
    points = generate_points(n)
    
    # Step 1: Generate all unique lines (deduplication)
    print("Generating unique lines...")
    
    # Represent lines in the form ax + by + c = 0
    line_dict = {}  # Use a dictionary for deduplication
    
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            p1, p2 = points[i], points[j]
            a = p2[1] - p1[1]  # y2 - y1
            b = p1[0] - p2[0]  # x1 - x2
            c = p1[1] * p2[0] - p1[0] * p2[1]  # y1*x2 - x1*y2
            
            # Normalize to avoid floating point issues
            gcd = math.gcd(math.gcd(abs(a), abs(b)), abs(c)) if c != 0 else math.gcd(abs(a), abs(b))
            if gcd > 0:
                if a < 0 or (a == 0 and b < 0):
                    gcd = -gcd
                a //= gcd
                b //= gcd
                c //= gcd
            
            # Use tuple as key for deduplication
            line_key = (a, b, c)
            line_dict[line_key] = True
    
    lines = list(line_dict.keys())
    M = len(lines)
    print(f"M(L{n}) = {M} (unique lines)")
    
    # For a more direct approach to counting intersections with the correct count
    # Group lines by slope for more efficient intersection counting
    print("Grouping lines by slope for efficient intersection counting...")
    
    # Group lines by their slopes
    slope_groups = defaultdict(list)
    for i, (a, b, c) in enumerate(lines):
        # For lines in format ax + by + c = 0, the slope is -a/b
        # Lines with same (a,b) values (after normalization) are parallel
        if b == 0:  # Vertical line
            slope_key = float('inf')  # Represent infinite slope
        else:
            slope_key = -a / b  # Standard slope formula
        
        slope_groups[slope_key].append((i, a, b, c))
    
    # Count intersections between lines in different slope groups
    S = 0
    slope_keys = list(slope_groups.keys())
    
    for i in range(len(slope_keys)):
        slope1 = slope_keys[i]
        lines_group1 = slope_groups[slope1]
        
        for j in range(i+1, len(slope_keys)):
            slope2 = slope_keys[j]
            lines_group2 = slope_groups[slope2]
            
            # If slopes are different, all lines in group 1 intersect all lines in group 2
            # Each intersection contributes 2 to the total (once for each line)
            intersection_pair_count = len(lines_group1) * len(lines_group2)
            S += 2 * intersection_pair_count
    
    elapsed = time.time() - start_time
    print(f"Calculation completed in {elapsed:.2f} seconds")
    print(f"S(L{n}) = {S}")
    return M, S

def solve(n):
    start_time = time.time()
    print(f"Generating {n} points...")
    points = generate_points(n)
    
    # Step 1: Generate all unique lines
    print("Generating unique lines...")

    print(points[:100])
    
    # Represent lines in the form ax + by + c = 0
    lines = []
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            p1, p2 = points[i], points[j]
            a = p2[1] - p1[1]  # y2 - y1
            b = p1[0] - p2[0]  # x1 - x2
            c = p1[1] * p2[0] - p1[0] * p2[1]  # y1*x2 - x1*y2
            
            # Normalize to avoid floating point issues
            gcd = math.gcd(math.gcd(abs(a), abs(b)), abs(c)) if c != 0 else math.gcd(abs(a), abs(b))
            if gcd > 0:
                if a < 0 or (a == 0 and b < 0):
                    gcd = -gcd
                a //= gcd
                b //= gcd
                c //= gcd
            
            lines.append((a, b, c))
    
    # Remove duplicates
    unique_lines = []
    seen = set()
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)
    
    lines = unique_lines
    M = len(lines)
    print(f"M(L{n}) = {M} (unique lines)")
    
    # Group lines by slope
    print("Grouping lines by slope...")
    slope_groups = defaultdict(list)
    for i, (a, b, c) in enumerate(lines):
        # Lines with same (a,b) are parallel
        slope_key = (a, b)
        slope_groups[slope_key].append((i, c))
    
    # Step 2: Calculate intersections
    print("Calculating intersections...")
    
    # Two lines (a1,b1,c1) and (a2,b2,c2) intersect if and only if a1*b2 != a2*b1 (non-parallel)
    S = 0
    group_count = len(slope_groups)
    progress_step = max(1, group_count // 20)
    processed_groups = 0
    
    slope_keys = list(slope_groups.keys())
    for i in range(len(slope_keys)):
        if i % progress_step == 0:
            elapsed = time.time() - start_time
            print(f"Processing group {i+1}/{group_count}, elapsed: {elapsed:.2f}s")
            
        slope1 = slope_keys[i]
        lines1 = slope_groups[slope1]
        
        for j in range(i+1, len(slope_keys)):
            slope2 = slope_keys[j]
            lines2 = slope_groups[slope2]
            
            # Check if these slopes can intersect (non-parallel)
            det = slope1[0] * slope2[1] - slope1[1] * slope2[0]
            if det == 0:  # Parallel lines don't intersect
                continue
                
            # Every line in group1 intersects with every line in group2
            # Each intersection counts twice (once for each line)
            S += 2 * len(lines1) * len(lines2)
    
    elapsed = time.time() - start_time
    print(f"Calculation completed in {elapsed:.2f} seconds")
    print(f"S(L{n}) = {S}")
    return M, S

def visualize_points(n):
    """
    Create a scatter plot visualization of the first n points.
    """
    points = generate_points(n)
    x_coords, y_coords = zip(*points)
    
    plt.figure(figsize=(10, 10))
    plt.scatter(x_coords, y_coords, color='blue', alpha=0.7, s=20)
    plt.grid(True)
    plt.title(f'L{n}: {n} points generated by Project Euler problem 630')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    # Set equal aspect ratio so the plot isn't stretched
    plt.axis('equal')
    
    # Show the range of coordinates (-1000 to 1000 in both dimensions)
    plt.xlim(-1000, 1000)
    plt.ylim(-1000, 1000)
    
    plt.savefig(f'L{n}_points.png')
    plt.show()

def visualize_lines(n, max_lines=50):
    """
    Create a visualization of the first max_lines unique lines from L(n).
    """
    points = generate_points(n)
    
    # Generate unique lines
    line_dict = {}
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            p1, p2 = points[i], points[j]
            a = p2[1] - p1[1]  # y2 - y1
            b = p1[0] - p2[0]  # x1 - x2
            c = p1[1] * p2[0] - p1[0] * p2[1]  # y1*x2 - x1*y2
            
            # Normalize
            gcd = math.gcd(math.gcd(abs(a), abs(b)), abs(c)) if c != 0 else math.gcd(abs(a), abs(b))
            if gcd > 0:
                if a < 0 or (a == 0 and b < 0):
                    gcd = -gcd
                a //= gcd
                b //= gcd
                c //= gcd
            
            line_dict[(a, b, c)] = (p1, p2)
    
    unique_lines = list(line_dict.items())[:max_lines]
    
    # Plot points
    plt.figure(figsize=(12, 12))
    x_coords, y_coords = zip(*points)
    plt.scatter(x_coords, y_coords, color='blue', alpha=0.7, s=20)
    
    # Plot lines
    for (a, b, c), (p1, p2) in unique_lines:
        if b == 0:  # Vertical line
            x = -c / a
            plt.axvline(x=x, color='red', alpha=0.3)
        else:
            # Generate two points for the line
            x_min, x_max = -1100, 1100
            y_min = (-a * x_min - c) / b
            y_max = (-a * x_max - c) / b
            plt.plot([x_min, x_max], [y_min, y_max], 'r-', alpha=0.3)
    
    plt.grid(True)
    plt.title(f'L{n}: First {len(unique_lines)} unique lines through points')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.5)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.5)
    
    # Set equal aspect ratio
    plt.axis('equal')
    plt.xlim(-1100, 1100)
    plt.ylim(-1100, 1100)
    
    plt.savefig(f'L{n}_lines.png')
    plt.show()

# Verify with test cases
print("\nTesting with n=3:")
solve(3)
print("\nTesting with n=100:")
M100, S100 = solve(100)
print(f"Expected: M(L100) = 4948, S(L100) = 24477690")
if M100 != 4948 or S100 != 24477690:
    print("ERROR: Test case failed!")
    exit(1)
else:
    print("Test case passed!")

# Test the sweep-line algorithm
print("\nTesting sweep-line algorithm with n=3:")
solve_sweep_line(3)

print("\nTesting sweep-line algorithm with n=100:")
M100, S100 = solve_sweep_line(100)
print(f"Expected: M(L100) = 4948, S(L100) = 24477690")
if M100 != 4948 or S100 != 24477690:
    print("ERROR: Sweep-line algorithm test case failed!")
else:
    print("Sweep-line test case passed!")

# Visualize L100 points
M2500, L2500 = solve_sweep_line(2500)

print(M2500, L2500)