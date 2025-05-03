#include <iostream>
#include <vector>
#include <unordered_map>
#include <set>
#include <cmath>
#include <algorithm>
#include <climits>

// Calculate r = -(1 - p*q)/(p + q)
long long calculate_r(long long p, long long q) {
    // Avoid division by zero
    if (p + q == 0) {
        return LLONG_MAX; // Representing None/null
    }
    
    // Use double for intermediate calculation to avoid overflow
    double r_val = (1.0 - p * q) / (p + q);
    return -static_cast<long long>(r_val);
}

// Precompute primes up to max_p using Sieve of Eratosthenes - O(p) space
std::vector<long long> precompute_primes(long long max_p) {
    std::vector<bool> is_prime(max_p + 1, true);
    std::vector<long long> primes;
    
    // 0 and 1 are not prime
    is_prime[0] = is_prime[1] = false;
    
    for (long long i = 2; i <= max_p; i++) {
        if (is_prime[i]) {
            primes.push_back(i);
            // Mark multiples as non-prime
            for (long long j = i * i; j <= max_p && j > 0; j += i) { // Check j > 0 to prevent overflow
                is_prime[j] = false;
            }
        }
    }
    
    return primes;
}

// Function to factorize n using precomputed primes
std::unordered_map<long long, int> factorize(long long n, const std::vector<long long>& primes) {
    std::unordered_map<long long, int> factors;
    
    for (long long prime : primes) {
        // Optimization: p² + 1 is never divisible by primes of form 4k+3
        if (prime > 2 && prime % 4 == 3) continue;
        
        if (prime * prime > n) break;
        
        while (n % prime == 0) {
            factors[prime]++;
            n /= prime;
        }
    }
    
    // If n > 1, it's a prime factor itself
    if (n > 1) factors[n] = 1;
    
    return factors;
}

// Generate all divisors from prime factorization
std::vector<long long> generate_divisors(const std::unordered_map<long long, int>& factors) {
    std::vector<long long> divisors = {1};
    
    for (const auto& [prime, count] : factors) {
        int size = divisors.size();
        long long power = 1;
        
        for (int i = 0; i < count; i++) {
            power *= prime;
            for (int j = 0; j < size; j++) {
                divisors.push_back(divisors[j] * power);
            }
        }
    }
    
    return divisors;
}

// Check if p, q, r satisfy the condition
bool actually_fine(long long p, long long q, long long r) {
    return p * q * r > 0 && p*q + q*r + r*p == 1;
}

// Find positive products using an optimized divisor method with O(p) space complexity
std::unordered_map<long long, bool> find_positive_products_optimized(
    long long max_p = 50, 
    long long min_product = 1, 
    long long max_product = 10000) {
    
    std::unordered_map<long long, std::vector<std::vector<long long>>> positive_results;
    
    // Precompute primes up to max_p for efficient factorization
    std::vector<long long> primes = precompute_primes(max_p);

    std::unordered_map<long long, bool> combo;
    
    for (long long p = 1; p <= max_p; ++p) {
        // Calculate 1 + p²
        long long p_squared_plus_1 = 1 + p*p;
        
        if (p % 10000 == 0) {
            std::cout << "Done " << p << std::endl;
        }
        
        // Factorize p² + 1 and generate its divisors
        std::unordered_map<long long, int> factors = factorize(p_squared_plus_1, primes);
        std::vector<long long> divisors = generate_divisors(factors);
        
        // Sort divisors for better cache locality
        std::sort(divisors.begin(), divisors.end());
        
        for (long long d : divisors) {
            // Calculate q from the divisor
            long long q = d - p;

            combo[p*(p+d)*((p*p+1)/d + p)] = true;
            
         
        }
    }
    
    return combo;
}

int main() {
    std::cout << "Running optimized divisor method to find positive products..." << std::endl;
    
    // Run the optimized finder
    auto products_dict = find_positive_products_optimized(50000, 1, 1e18);

    std::cout << "Size:" << products_dict.size() << std::endl;


    std::vector<long long> prod;
    for(auto & [k, _]: products_dict) {
        prod.push_back(k);
    }
    
    std::sort(prod.begin(), prod.end());

    for(auto i = 0u ; i < std::min(static_cast<size_t>(10), prod.size()); ++i) {
        std::cout << prod[i] << std::endl;
    }

    if(products_dict.size() >= 150000) {
        std::cout << "150000th: "  << prod[150000 - 1] <<std::endl;
    }
   
    
    return 0;
}
