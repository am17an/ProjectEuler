#include <iostream>
#include <vector>
#include <unordered_map>
#include <list>
#include <algorithm>
#include <thread>
#include <mutex>
#include <atomic>
#include <chrono>

// Smaller, more focused LRU Cache implementation
class LRUCache {
private:
    const int capacity;
    std::list<std::pair<long long, long long>> items;
    std::unordered_map<long long, std::list<std::pair<long long, long long>>::iterator> cache;
    std::atomic<size_t> hit_count{0};
    std::atomic<size_t> miss_count{0};

public:
    LRUCache(int size) : capacity(size) {
        // Reserve space to avoid rehashing
        cache.reserve(size);
    }

    void clear() {
        cache.clear();
        items.clear();
    }

    double hit_ratio() const {
        size_t total = hit_count + miss_count;
        return total > 0 ? static_cast<double>(hit_count) / total : 0.0;
    }

    size_t size() const {
        return cache.size();
    }

    long long get(long long key) {
        auto it = cache.find(key);
        if (it == cache.end()) {
            miss_count++;
            return -1; // Not found
        }
        
        hit_count++;
        // Move to front (most recently used)
        items.splice(items.begin(), items, it->second);
        return it->second->second;
    }

    void put(long long key, long long value) {
        auto it = cache.find(key);
        
        // If found, update value and move to front
        if (it != cache.end()) {
            it->second->second = value;
            items.splice(items.begin(), items, it->second);
            return;
        }
        
        // If cache is full, remove least recently used item
        if (cache.size() >= capacity) {
            auto last = items.back();
            cache.erase(last.first);
            items.pop_back();
        }
        
        // Insert new item at front
        items.emplace_front(key, value);
        cache[key] = items.begin();
    }
};

// Calculate GCD
int gcd(long long a, long long b) {
    while (b) {
        long long t = b;
        b = a % b;
        a = t;
    }
    return a;
}

// Calculate prime factorization of n
std::vector<std::pair<long long, int>> prime_factorize(long long n) {
    std::vector<std::pair<long long, int>> factors;
    factors.reserve(8); // Reserve space for a typical number of prime factors
    
    for (long long p = 2; p * p <= n; ++p) {
        if (n % p == 0) {
            int exp = 0;
            while (n % p == 0) {
                n /= p;
                exp++;
            }
            factors.push_back({p, exp});
        }
    }
    
    if (n > 1) {
        factors.push_back({n, 1});
    }
    
    return factors;
}

// Generate all divisors from prime factorization
void generate_divisors(const std::vector<std::pair<long long, int>>& factors, 
                       size_t idx, long long current, std::vector<long long>& divisors) {
    if (idx == factors.size()) {
        divisors.push_back(current);
        return;
    }
    
    auto [prime, max_exp] = factors[idx];
    long long p_power = 1;
    
    for (int exp = 0; exp <= max_exp; ++exp) {
        generate_divisors(factors, idx + 1, current * p_power, divisors);
        p_power *= prime;
    }
}

// Calculate totient and find divisors in one go - with optimization
std::pair<long long, std::vector<long long>> totient_and_divisors(long long n) {
    auto factors = prime_factorize(n);
    
    // Calculate totient using the prime factorization
    long long phi = n;
    for (const auto& [p, _] : factors) {
        phi -= phi / p;
    }
    
    // Generate divisors of phi
    std::vector<long long> divisors;
    divisors.reserve(64); // Reserve reasonable space
    generate_divisors(prime_factorize(phi), 0, 1, divisors);
    std::sort(divisors.begin(), divisors.end());
    
    return {phi, divisors};
}

// Fast modular exponentiation
long long mod_pow(long long base, long long exp, long long mod) {
    long long result = 1;
    base %= mod;
    
    while (exp > 0) {
        if (exp & 1) {
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exp >>= 1;
    }
    
    return result;
}

// Find multiplicative order of 10 modulo K
long long find_order_10_mod_k(long long K, LRUCache& cache) {
    // Check if result is already in cache
    long long cached_result = cache.get(K);
    if (cached_result != -1) {
        return cached_result;
    }
    
    // If gcd(10, K) != 1, order doesn't exist
    if (gcd(10, K) != 1) {
        cache.put(K, 0);
        return 0;
    }
    
    // Calculate phi(K) and divisors in one go
    auto [phi_k, divs] = totient_and_divisors(K);
    
    // Find order using binary exponentiation
    for (long long d : divs) {
        if (mod_pow(10, d, K) == 1) {
            cache.put(K, d);
            return d;
        }
    }
    
    cache.put(K, 0);
    return 0;
}

// Thread worker function
void worker_function(long long start, long long end, std::atomic<long long>& total_sum) {
    using namespace std::chrono;
    
    long long local_sum = 0;
    long long processed = 0;
    auto start_time = high_resolution_clock::now();
    
    // Create a local LRU cache with limited size (adjust as needed)
    LRUCache local_cache(5000); // Smaller cache size
    
    // Pre-populate with some common values
    //local_cache.put(1, 1);
    
    for (long long i = start; i < end; ++i) {
        processed++;
        
        // Periodically check cache performance and reset if needed
        if (processed % 1000000 == 0) {
            auto current_time = high_resolution_clock::now();
            double elapsed = duration_cast<milliseconds>(current_time - start_time).count() / 1000.0;
            double hit_ratio = local_cache.hit_ratio();
            
            std::cout << "Thread " << std::this_thread::get_id() 
                      << " processed " << processed << " numbers"
                      << " (" << processed / elapsed << " nums/sec)"
                      << " Cache hit ratio: " << hit_ratio * 100.0 << "%" 
                      << " Size: " << local_cache.size() << std::endl;
            
            // If cache hit ratio is too low, clear it to save memory
            local_cache.clear();
            local_cache.put(1, 1); // Add basic values back
        }
        
        // Skip simple cases
        if (i % 2 == 0 || i % 5 == 0) {
            // Remove factors of 2 and 5
            long long n = i;
            while (n % 2 == 0) {
                n /= 2;
            }
            while (n % 5 == 0) {
                n /= 5;
            }
            
            if (n == 0) {
                continue;
            }
            
            // Only compute for the reduced number
            long long order = find_order_10_mod_k(n, local_cache);
            if (order > 0) {
                local_sum += order;
            }
        } else {
            // Numbers not divisible by 2 or 5 are processed directly
            long long order = find_order_10_mod_k(i, local_cache);
            if (order > 0) {
                local_sum += order;
            }
        }
    }
    
    auto end_time = high_resolution_clock::now();
    double elapsed = duration_cast<milliseconds>(end_time - start_time).count() / 1000.0;
    std::cout << "Thread " << std::this_thread::get_id() 
              << " finished " << (end - start) << " numbers in " << elapsed << " seconds"
              << " (" << (end - start) / elapsed << " nums/sec)"
              << " Final cache hit ratio: " << local_cache.hit_ratio() * 100.0 << "%" << std::endl;
    
    // Update total sum
    total_sum += local_sum;
}

int main() {
    using namespace std::chrono;
    
    const long long limit = 1e8;
    const long long batch_size = 5'000'000;  // Larger batch size
    
    // Fixed number of threads
    unsigned int num_threads = std::max(1u, 8u);
    std::cout << "Using " << num_threads << " threads" << std::endl;
    
    std::atomic<long long> total_sum(0);
    auto global_start_time = high_resolution_clock::now();
    
    for (long long batch_start = 3; batch_start <= limit; batch_start += batch_size) {
        long long batch_end = std::min(batch_start + batch_size, limit);
        
        auto batch_start_time = high_resolution_clock::now();
        std::cout << "Processing batch " << batch_start << " to " << batch_end - 1 << std::endl;
        
        std::vector<std::thread> threads;
        long long chunk_size = (batch_end - batch_start) / num_threads;
        
        for (unsigned int t = 0; t < num_threads; ++t) {
            long long chunk_start = batch_start + t * chunk_size;
            long long chunk_end = (t == num_threads - 1) ? batch_end : chunk_start + chunk_size;
            
            threads.emplace_back(worker_function, chunk_start, chunk_end, std::ref(total_sum));
        }
        
        // Wait for all threads to complete
        for (auto& thread : threads) {
            thread.join();
        }
        
        auto batch_end_time = high_resolution_clock::now();
        double batch_elapsed = duration_cast<milliseconds>(batch_end_time - batch_start_time).count() / 1000.0;
        
        std::cout << "Batch completed in " << batch_elapsed << " seconds"
                  << " (" << (batch_size / batch_elapsed) << " nums/sec)" << std::endl;
        std::cout << "Current sum: " << total_sum << std::endl;
    }
    
    auto global_end_time = high_resolution_clock::now();
    double total_elapsed = duration_cast<milliseconds>(global_end_time - global_start_time).count() / 1000.0;
    
    std::cout << "Final result: " << total_sum << std::endl;
    std::cout << "Total time: " << total_elapsed << " seconds" 
              << " (" << (limit / total_elapsed) << " nums/sec)" << std::endl;
    
    return 0;
} 