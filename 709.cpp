#include <iostream> 
#include <vector>
#include <iomanip>

static constexpr int N = 24681;  // Changed to 10
//static constexpr int N = 9;  // Changed to 10
static constexpr int MOD = 1020202009;

std::vector<std::vector<int>> dp(2, std::vector<int>(N));
std::vector<std::vector<int>> binom(N, std::vector<int>(N));

void print_state(int day, int prev) {
    std::cout << "\nDay " << day << " state:\n";
    std::cout << "Bags:  ";
    for(int i = 0; i <= day; i++) {
        std::cout << std::setw(8) << i << " ";
    }
    std::cout << "\nCount: ";
    for(int i = 0; i <= day; i++) {
        std::cout << std::setw(8) << dp[prev][i] << " ";
    }
    std::cout << "\n";

    // Print sum for this day
    int sum = 0;
    for(int i = 0; i <= day; i++) {
        sum = (sum + dp[prev][i]) % MOD;
    }
    std::cout << "Sum for day " << day << ": " << sum << "\n";
}

void calc_binom() {
    // Initialize first column
    for (int i = 0; i < N; i++) {
        binom[i][0] = 1;
    }
    
    // Compute binomial coefficients using Pascal's triangle
    for (int i = 1; i < N; i++) {
        for (int j = 1; j <= i; j++) {
            binom[i][j] = (binom[i-1][j] + binom[i-1][j-1]) % MOD;
        }
    }
}

int solve(int n) {
    // Initialize both rows to 0
    for (int i = 0; i < N; i++) {
        dp[0][i] = 0;
        dp[1][i] = 0;
    }

    calc_binom();
    dp[0][0] = 1;
    int curr = 1, prev = 0;

    for (int days = 1; days < n; days++) {

        if(days%100 == 0) {
            std::cout << "doing " << days << std::endl;
        }
        // Clear current row
        for (int i = 0; i < N; i++) {
            dp[curr][i] = 0;
        }

        // Process all positions but only update matching parity
        for(int bags = 1; bags <= days; bags++) {
            // For odd days, only update odd positions
            // For even days, only update even positions
            if ((days % 2) == (bags % 2)) {
                //just the one bag
                dp[curr][bags] += dp[prev][bags-1];
                dp[curr][bags] %= MOD;
            }

            for(int k = 2; k <= bags; k += 2) {
                int target = bags-k+1;
                // Only update if target position matches day's parity
                if ((days % 2) == (target % 2)) {
                    dp[curr][target] += (static_cast<int64_t>(binom[bags][k]) * static_cast<int64_t>(dp[prev][bags]))%MOD;
                    dp[curr][target] %= MOD;
                }
            }
        }
        
        // Swap current and previous rows
        std::swap(curr, prev);
        //print_state(days, prev);
    }

    int total = 0;
    for(int i = 0; i < N; ++i) {
        total += dp[prev][i];
        total %= MOD;
    }

    return total;
}

int main() {
    int result = solve(N);

    std::cout << "Result: " << result << std::endl;
    return 0;
}