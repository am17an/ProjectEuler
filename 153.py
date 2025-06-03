
from sympy import gcd

def fast_sum_series(N, norm, a):
    total = 0
    max_k = N // norm
    
    # Group by the value of floor(N/(norm*k))
    v = 1
    while v <= max_k:
        # Find range of k where floor(N/(norm*k)) = v
        # This happens when: v <= N/(norm*k) < v+1
        # Rearranging: N/(v+1) < norm*k <= N/v
        # So: N/((v+1)*norm) < k <= N/(v*norm)
        
        L = max(1, N // ((v + 1) * norm) + 1)
        R = min(max_k, N // (v * norm))
        
        if L <= R:
            # Sum of k from L to R is (R-L+1)*(L+R)/2
            sum_k = (R - L + 1) * (L + R) // 2
            total += 2 * a * v * sum_k
            
        v += 1
    
    return total

def sum_gaussian_divisors_real_parts_optimized(N):
    total = 0
    
    # Add regular integer divisors
    for n in range(1, N + 1):
        total += (N//n)*n
    
    # Add contributions from non-real Gaussian integers
    print(total)
    limit = int(N ** 0.5) + 1
    
    count = 0
    for a in range(1, limit + 1):
        if a%1000 == 0:
            print("Done ", a)
        print(a)
        for b in range(a, limit + 1):
            if a > b:  # Avoid double counting (a,b) and (b,a)
                continue
            count += 1

            if gcd(a, b) != 1:
                continue
                
            norm = a*a + b*b
            if norm > N:
                break
            
            #print("For norm ", norm, " multiples", multiples)
            
            if a == b:
                # Divisors: a+ai, a-ai
                #total += 2 * a * multiples
                total += fast_sum_series(N, norm, a)
            else:
                # Divisors: a+bi, a-bi, b+ai, b-ai  
                total += fast_sum_series(N, norm, a+b)
            #print("Norm", norm, total)
    
    #print(count)
    return total

# Test
print(f"Sum for N=5: {sum_gaussian_divisors_real_parts_optimized(5)}")
print(f"Sum for N=10: {sum_gaussian_divisors_real_parts_optimized(10)}")
print(f"Sum for N=10: {sum_gaussian_divisors_real_parts_optimized(10**8)}")