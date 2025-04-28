#include <iostream>
static constexpr int64_t mod = 1e17;

int64_t choose[19][19];

void precompute() { 
    for(int i = 0; i < 19; ++i) {
        choose[i][0] = 1;
        for(int j = 1; j <= i; ++j) {
            choose[i][j] = (choose[i-1][j] + choose[i-1][j-1]) % mod;
        }
    }
}

int64_t power(int base, int exp) {

    // do binary exponentiation
    int64_t result = 1;
    while(exp > 0) {
        if(exp % 2 == 1) {
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exp /= 2;
    }
    return result;
}

int64_t solve(int numDigits) {

    int64_t ans = 0;
    for(int digit = 1 ; digit <= 9; ++digit) {
        for(int numZeros = 0; numZeros < numDigits; ++numZeros) {
            int numNonZero = numDigits - numZeros - 1;
            int numWays = power(10 - digit, numNonZero+1) - power(9 - digit, numNonZero+1);

            numWays = (numWays * choose[numDigits-1][numZeros]) % mod;

            std::cout << "Digit:" << digit << " numZeros:" << numZeros << " numNonZero:" << numNonZero << " numWays:" << numWays << " " << numWays*power(10, numNonZero)*digit << std::endl;

            ans = (ans + numWays*power(10, numNonZero)*digit) % mod;

        }
    }

    return ans;
}

int main() {

    precompute();

    int64_t ans = 0;
    for(int i = 1; i <= 2; ++i) {
        ans = (ans + solve(i)) % mod;
    }
    std::cout << ans << std::endl;
}