#include <iostream>
using namespace std;

// Define the modulo as per the problem
const int64_t MOD = 1e16;

// Fast exponentiation for calculating powers
int64_t power(int64_t base, int64_t exp) {
    int64_t result = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp & 1) result = (result * base) % MOD;
        base = (base * base) % MOD;
        exp >>= 1;
    }
    return result;
}

// Calculate S(n) using proper dynamic programming
int64_t calculateS(int n) {
    // For large n, we need a memory-efficient approach
    // We'll use two 2D arrays for current and previous digit length
    int64_t dp_cnt[2][10][19] = {0};   // Count of numbers
    int64_t dp_sum[2][10][19] = {0};   // Sum of numbers
    
    // Base case: 1-digit numbers (1-9)
    for (int d = 1; d <= 9; d++) {
        dp_cnt[1 % 2][d][d] = 1;        // Count: one way to form digit d
        dp_sum[1 % 2][d][d] = d;        // Sum: just the digit d itself
    }
    
    // Track the total sum across all digits
    int64_t total_result = 0;
    
    // Add contribution of 1-digit DS-numbers to result
    for (int d = 1; d <= 9; d++) {
        if (d * 2 == d) {  // Only true for d=0, which isn't a valid 1-digit number
            total_result = (total_result + dp_sum[1 % 2][d][d]) % MOD;
        }
    }
    
    // Fill DP arrays for digits from 2 to n
    for (int digits = 2; digits <= n; digits++) {
        int curr = digits % 2;
        int prev = (digits - 1) % 2;
        
        // Reset current arrays
        for (int m = 0; m <= 9; m++) {
            for (int s = 0; s <= 18; s++) {
                dp_cnt[curr][m][s] = 0;
                dp_sum[curr][m][s] = 0;
            }
        }
        
        // Compute values for current digit length
        for (int prev_max = 0; prev_max <= 9; prev_max++) {
            for (int prev_sum = 0; prev_sum <= 18; prev_sum++) {
                if (dp_cnt[prev][prev_max][prev_sum] == 0) continue;
                
                // Try adding each possible new digit (0-9)
                for (int new_digit = 0; new_digit <= 9; new_digit++) {
                    int new_max = max(prev_max, new_digit);
                    int new_sum = prev_sum + new_digit;
                    
                    if (new_sum > 18) continue;  // Skip if sum exceeds 18
                    
                    // Update count
                    dp_cnt[curr][new_max][new_sum] = 
                        (dp_cnt[curr][new_max][new_sum] + dp_cnt[prev][prev_max][prev_sum]) % MOD;
                    
                    // Calculate contribution to sum:
                    // 1. All previous numbers * 10 (shift left)
                    int64_t shift_contrib = (dp_sum[prev][prev_max][prev_sum] * 10) % MOD;
                    
                    // 2. New digit in 1's place for each previous number
                    int64_t digit_contrib = (dp_cnt[prev][prev_max][prev_sum] * new_digit) % MOD;
                    
                    // Update sum
                    dp_sum[curr][new_max][new_sum] = 
                        (dp_sum[curr][new_max][new_sum] + shift_contrib + digit_contrib) % MOD;
                }
            }
        }
        
        // Add contribution of current digit length to result
        for (int max_digit = 0; max_digit <= 9; max_digit++) {
            int sum = max_digit * 2;
            if (sum <= 18) {
                total_result = (total_result + dp_sum[curr][max_digit][sum]) % MOD;
            }
        }
    }
    
    return total_result;
}

int main() {
    // Test for n=3
    cout << "S(3) = " << calculateS(3) << endl;
    cout << "Expected: 63270" << endl;
    
    // Test for n=7
    cout << "S(7) = " << calculateS(7) << endl;
    cout << "Expected: 85499991450" << endl;
    
    // Calculate S(2020)
    cout << "S(2020) = " << calculateS(2020) << endl;
    
    return 0;
}