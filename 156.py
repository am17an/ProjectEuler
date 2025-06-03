from matplotlib import pyplot as plt

def count_d(d, digit):
    return sum([r == digit for r in str(d)])

def brute_solve(n, d):
    total = 0
    for i in range(0, n+1):
        total += count_d(i, str(d))
    return total

def solve(n, d):
    if n == 0:
        return 0
        
    digits = []
    original_n = n
    while n != 0:
        digits.append(n%10)
        n //= 10

    ans = 0
    digits = digits[::-1]
    power10 = 10**(len(digits)-1)
    current = len(digits)

    for digit in digits:
        if digit > d:
            ans += power10
        elif digit == d:
            ans += original_n % (power10) + 1
        ans += digit*(current-1)*(power10//10)
        current -= 1
        power10 //= 10

    return ans

def binary_search_fixed_points(d, start, end, found_points=None):
    """
    Simple binary search to find all fixed points where solve(n, d) == n
    """
    if found_points is None:
        found_points = []
    
    # Base case: if range is small enough, check each number
    if end - start <= 1000:
        for n in range(max(1, start), end + 1):
            if solve(n, d) == n:
                found_points.append(n)
        return found_points
    
    # Check endpoints
    if start >= 1 and solve(start, d) == start:
        found_points.append(start)
    if solve(end, d) == end:
        found_points.append(end)
    
    # Calculate midpoint and check it
    mid = (start + end) // 2
    if solve(mid, d) == mid:
        found_points.append(mid)
    
    # Calculate differences to decide whether to search each half
    f_start = solve(start, d) - start if start >= 1 else -start
    f_mid = solve(mid, d) - mid
    f_end = solve(end, d) - end
    
    # Search left half if there might be a crossing
    if f_start * f_mid <= 0 or abs(f_start) < (mid - start) or abs(f_mid) < (mid - start):
        binary_search_fixed_points(d, start, mid, found_points)
    
    # Search right half if there might be a crossing
    if f_mid * f_end <= 0 or abs(f_mid) < (end - mid) or abs(f_end) < (end - mid):
        binary_search_fixed_points(d, mid, end, found_points)
    
    return found_points

def find_all_fixed_points(d, max_range=10**12):
    """
    Find all fixed points for digit d up to max_range using binary search
    """
    print(f"Finding fixed points for d = {d} up to {max_range}...")
    
    fixed_points = binary_search_fixed_points(d, 1, max_range)
    
    # Remove duplicates and sort
    fixed_points = sorted(list(set(fixed_points)))
    
    # Verify all found points
    verified_points = []
    for point in fixed_points:
        if solve(point, d) == point:
            verified_points.append(point)
    
    print(f"Found {len(verified_points)} fixed points for d = {d}: {verified_points}")
    return verified_points

if __name__ == "__main__":
    total_sum = 0
    all_results = {}
    
    for d in range(1, 10):
        print(f"\n{'='*50}")
        print(f"Processing digit d = {d}")
        print(f"{'='*50}")
        
        fixed_points = find_all_fixed_points(d, max_range=10**12)
        digit_sum = sum(fixed_points)
        
        all_results[d] = {
            'fixed_points': fixed_points,
            'sum': digit_sum
        }
        
        total_sum += digit_sum
        
        print(f"Sum for d = {d}: {digit_sum}")
    
    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")
    
    for d in range(1, 10):
        result = all_results[d]
        print(f"d = {d}: {len(result['fixed_points'])} fixed points, sum = {result['sum']}")
        if len(result['fixed_points']) <= 20:  # Only show points if not too many
            print(f"       Points: {result['fixed_points']}")
    
    print(f"\nTotal sum for all digits d = 1 to 9: {total_sum}")