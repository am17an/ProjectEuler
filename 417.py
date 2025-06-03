from math import gcd
from sympy import totient, divisors
from functools import cache
import multiprocessing as mp
from itertools import islice

# Global cache with a Manager to share between processes
manager = mp.Manager()
order_cache = manager.dict()

@cache
def find_order_10_mod_k(K):
    if gcd(10, K) != 1:
        return None  # Order doesn't exist
    phi_k = totient(K)
    for d in sorted(divisors(phi_k)):
        if pow(10, d, K) == 1:
            return d
    return None

def process_number(n):
    """Process a single number and return its order if it exists."""
    # Check the shared cache first
    if n in order_cache:
        return order_cache[n]
    
    s = find_order_10_mod_k(n)
    result = s if s is not None else 0
    
    # Update the shared cache
    order_cache[n] = result
    return result

def generate_numbers_to_check(start, end):
    """Generate numbers to check after removing factors of 2 and 5."""
    numbers = []
    for i in range(start, end):
        n = i
        while n % 2 == 0:
            n //= 2
        while n % 5 == 0:
            n //= 5
        if n > 0:
            numbers.append(n)
    return numbers

if __name__ == "__main__":
    limit = int(1e8)
    batch_size = 1_000_000  # Process in large batches
    
    # Use all available cores except one
    num_processes = max(1, mp.cpu_count() - 1)
    
    # Initialize the multiprocessing pool
    pool = mp.Pool(processes=num_processes)
    
    total_count = 0
    
    # Process in batches to manage memory usage
    for start in range(3, limit, batch_size):
        end = min(start + batch_size, limit)
        
        # Get all numbers to check in this batch
        numbers_to_check = generate_numbers_to_check(start, end)
        
        # Process numbers in parallel
        results = pool.map(process_number, numbers_to_check, chunksize=1000)
        
        # Add batch results to total
        batch_sum = sum(results)
        total_count += batch_sum
        
        print(f"Processed {start} to {end-1}, current sum: {total_count}")
    
    # Clean up
    pool.close()
    pool.join()
    
    print(f"Final result: {total_count}")