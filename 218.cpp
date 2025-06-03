#include <iostream>
#include <algorithm>
#include <vector>
#include <cassert>
#include <cmath>
#include <iomanip>

std::vector<int64_t> squares;
// Primes of form 4k+3 that we'll check
const std::vector<int> primes_4k3 = {3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83};

// Check if n is divisible by p at all
bool is_divisible_by(int64_t n, int p) {
    return n % p == 0;
}

// Check if n can be expressed as sum of two squares (hypotenuse)
bool can_be_sum_of_squares(int64_t n) {
    // Check constraints: must be of form 4n+1, cannot be divisible by 4, must be odd
    if (n % 2 == 0 || n % 4 == 0 || n % 4 != 1) {
        return false;
    }
    
    // For a number to be a hypotenuse, it cannot have ANY prime factor of form 4k+3
    for (int p : primes_4k3) {
        if (is_divisible_by(n, p)) {
            return false;
        }
    }
    return true;
}

int64_t is_square(int64_t n) {
    if(auto it = std::lower_bound(squares.begin(), squares.end(), n); it != squares.end() && *it == n) {
        return static_cast<int64_t>(it - squares.begin()) + 1;
    }
    return 0;
}

int main() {
    std::cout << "Starting calculation with limit: 1e16" << std::endl;
    int64_t q = 1;
    int64_t limit = 1e16;
    int count = 0;

    int checked = 0;
    int64_t progress_interval = 100000;
    
    while(q*q <= limit) {
        squares.push_back(q*q);
        q += 1;

        // Skip even values of q since c = q² must be odd and of form 4n+1
        if (q % 2 == 0) {
            continue;
        }
        
        // Show progress periodically
        if (checked % progress_interval == 0) {
            std::cout << "Progress: q = " << q << ", current count = " << count 
                      << ", q² = " << std::fixed << std::setprecision(0) << static_cast<double>(q)*q 
                      << " (" << std::setprecision(2) << (static_cast<double>(q)*q * 100.0 / limit) << "%)" 
                      << std::endl;
        }
        checked++;

        int64_t c = q*q;
        
        // Verify c is of form 4n+1 - this should always be true for odd q
        assert(c % 4 == 1);
        
        // Skip if c cannot be sum of two squares
        if (!can_be_sum_of_squares(c)) {
            continue;
        }

        for(int64_t m = 1; m*m < c; m++) {
            if(m%3 == 0 || m%7 == 0) continue;

            int64_t n_square = c - m*m;

            if(n_square >= m*m) continue;

            if(int64_t n = is_square(n_square); n!= 0 and n%3 != 0 and n%7 != 0) {
                //std::cout << "Triple " << m*m - n*n << " " << 2*m*n << " " << m*m + n*n << std::endl;
                //assert(m*m + n*n == c);
                int64_t area = (m+n)*(m-n)*m*n;
                if(area%6 != 0 || area%28 != 0) {
                    std::cout << "Triple " << m*m - n*n << " " << 2*m*n << " " << m*m + n*n << std::endl;
                    count++;
                }
            }
        }
    }

    std::cout << "\nFinal result: " << count << std::endl;
}