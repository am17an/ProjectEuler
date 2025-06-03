#include <iostream>
#include <unordered_map>
#include <vector>
#include <cmath>
#include <algorithm>
#include <thread>
#include <mutex>
#include <future>

// Fast modular exponentiation: calculates (base^exp) % mod
long long mod_pow(long long base, long long exp, long long mod) {
    if (mod == 1) return 0;
    
    long long result = 1;
    base %= mod;
    
    while (exp > 0) {
        if (exp & 1) {
            result = (result * base) % mod;
        }
        exp >>= 1;
        base = (base * base) % mod;
    }
    
    return result;
}

// Calculate nth digit of 1/d directly
int find_digit_direct(long long d, long long n) {
    // If n is too large or d is 1, return 0
    if (n <= 0 || d == 1) {
        return 0;
    }
    
    // Calculate 10^(n-1) mod d and then multiply by 10 and divide by d
    long long numerator = mod_pow(10, n - 1, d);
    return (numerator * 10) / d;
}

// Calculate S(n) using multithreading
long long calculate_S(long long n) {
    long long result = 0;
    const int BATCH_SIZE = 10000;
    const int num_threads = std::thread::hardware_concurrency();
    std::mutex result_mutex;
    
    auto process_batch = [&](long long start, long long end, long long digit_pos) {
        long long local_sum = 0;
        for (long long i = start; i <= end; i++) {
            local_sum += find_digit_direct(i, digit_pos);
        }
        
        // Safely add to the result
        std::lock_guard<std::mutex> lock(result_mutex);
        result += local_sum;
    };
    
    std::vector<std::future<void>> futures;
    
    for (long long batch_start = 1; batch_start <= n; batch_start += BATCH_SIZE) {
        long long batch_end = std::min(batch_start + BATCH_SIZE - 1, n);
        
        if (futures.size() >= num_threads) {
            futures[0].get();
            futures.erase(futures.begin());
        }
        
        futures.push_back(std::async(std::launch::async, process_batch, batch_start, batch_end, n));
    }
    
    for (auto& future : futures) {
        future.get();
    }
    
    return result;
}

int main() {
    // Verify that S(100) = 418
    std::cout << "Calculating S(100)..." << std::endl;
    long long s_100 = calculate_S(100);
    std::cout << "S(100) = " << s_100 << std::endl;
    if (s_100 == 418) {
        std::cout << "Verification passed: S(100) = 418" << std::endl;
        
        // Calculate S(10^7) if verification passes
        const long long LIMIT = 10000000; // 10^7
        std::cout << "Do you want to calculate S(10^7)? (y/n): ";
        char response;
        std::cin >> response;
        
        if (response == 'y' || response == 'Y') {
            std::cout << "Calculating S(10^7)..." << std::endl;
            long long result = calculate_S(LIMIT);
            std::cout << "S(10^7) = " << result << std::endl;
        }
    } else {
        std::cout << "Verification failed: S(100) should be 418, but got " << s_100 << std::endl;
    }
    
    return 0;
}
