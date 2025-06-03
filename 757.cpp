#include <iostream>
#include <unordered_set>
#include <cmath>
#include <cstdint>

// For numbers up to 10^14, we need a different approach than a single bitset
// Using sparse storage with unordered_set is better for very large numbers

// Reserve capacity for the unordered_set to avoid rehashing
uint64_t countENumbers(uint64_t N) {
    std::unordered_set<uint64_t> results;
    results.reserve(100000000);  // Reserve space for expected number of results
    
    uint64_t max_a = static_cast<uint64_t>(sqrt(N));
    
    for (uint64_t a = 1; a <= max_a; ++a) {
        if (a % 1000000 == 0) {
            std::cout << "Progress: " << a << "/" << max_a << " (" << results.size() << " found)" << std::endl;
        }
        
        uint64_t a_sq = a * a;
        uint64_t sqrt_a_sq = a; // sqrt(a²) = a
        
        // Only need to iterate up to sqrt(a_sq) to find all divisors of a²
        for (uint64_t d = 1; d <= sqrt_a_sq; ++d) {
            if (a_sq % d == 0) {
                // Process divisor d
                uint64_t c = a + d;
                uint64_t E = c * a_sq / d;
                
                // Process the complementary divisor a²/d (if different)
                uint64_t d2 = a_sq / d;
                if (d != d2) { // Avoid duplicate when d = sqrt(a²)
                    uint64_t c2 = a + d2;
                    uint64_t E2 = c2 * a_sq / d2;
                    
                    if (E2 < N and (E2%c == 0 and E2%a == 0)) {
                        results.insert(E2);
                    }
                }
            }
        }
    }
    
    return results.size();
}

int main() {
    uint64_t N = 1e6; // 10^14
    std::cout << "Computing E numbers up to " << N << "..." << std::endl;
    uint64_t result = countENumbers(N);
    std::cout << "Result: " << result << std::endl;
    return 0;
} 