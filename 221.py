def calculate_r(p, q):
    """Calculate r = (1 - p*q)/(p + q)"""
    if p + q == 0:
        return None  # Avoid division by zero
    
    r_val = (1 - p * q) / (p + q)
    return -r_val

def find_divisors(n):
    """Efficiently find all divisors of n"""
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return divisors

def actually_fine(p, q, r):
    return p * q * r > 0 and p*q + q*r + r*p == 1

def find_positive_products_optimized(max_p=50, min_product=1, max_product=10000):
    """Find positive products using an optimized divisor method"""
    positive_results = {}  # Use a dictionary to store unique products
    
    for p in range(0, max_p + 1):
        if p == 0:
            continue
        
        # Calculate 1 + p²
        p_squared_plus_1 = 1 + p**2
        
        # Find all divisors of 1 + p²
        divisors = find_divisors(p_squared_plus_1)
        
        for d in divisors:
            # Calculate q from the divisor
            q = d - p
            
            if p + q == 0:
                continue
            
            # Calculate r
            r = calculate_r(p, q)
            
            # Verify r is an integer
            if r is not None and r == int(r):
                r = int(r)
                product = p * q * r
                
                # Only include positive products within our target range
                if product > 0:
                    if product not in positive_results:
                        positive_results[product] = []
                    
                    # Store only if we don't already have this combination
                    combination = (p, q, r)
                    if actually_fine(p, q, r) and combination not in [tuple(item[:3]) for item in positive_results[product]]:
                        positive_results[product].append([p, q, r, d])
    
    return positive_results

def analyze_patterns(products_dict):
    """Analyze patterns in the results"""
    # Count number of products with specific factors
    factor_counts = {}
    
    for product in products_dict:
        # Find prime factorization
        factors = prime_factorization(product)
        factor_str = factorization_to_string(factors)
        
        if factor_str not in factor_counts:
            factor_counts[factor_str] = 0
        factor_counts[factor_str] += 1
    
    print("\nPattern Analysis:")
    print("=================")
    print(f"Found {len(factor_counts)} unique factorization patterns")
    
    # Show most common patterns
    sorted_patterns = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)
    for pattern, count in sorted_patterns[:5]:
        print(f"Pattern '{pattern}' appears {count} times")

def prime_factorization(n):
    """Find the prime factorization of n"""
    factors = {}
    d = 2
    while n > 1:
        while n % d == 0:
            if d in factors:
                factors[d] += 1
            else:
                factors[d] = 1
            n //= d
        d += 1
        if d*d > n and n > 1:
            if n in factors:
                factors[n] += 1
            else:
                factors[n] = 1
            break
    return factors

def factorization_to_string(factors):
    """Convert a factorization dictionary to a string representation"""
    if not factors:
        return "1"
    return " × ".join(f"{prime}^{power}" if power > 1 else f"{prime}" for prime, power in sorted(factors.items()))

# Run the optimized finder
print("Running optimized divisor method to find positive products...")
products_dict = find_positive_products_optimized(100000, 1, 1e18)

# Display results
print(f"Found {sum(len(v) for v in products_dict.values())} combinations with positive products")
print(f"Number of unique products: {len(products_dict)}\n")

# Sort products and show the smallest ones
smallest_products = sorted(products_dict.keys())  # Show first 15 unique products

if len(smallest_products) >= 150000:
    print("Found 150000 products", smallest_products[5], smallest_products[149999])
else:
    print("Found", len(smallest_products), "products. Run Moar", ','.join(str(x) for x in smallest_products[:15]))
