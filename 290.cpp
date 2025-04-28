#include <iostream>
#include <vector>


static constexpr int MAX_SUM = 7*17 + 1;
int dp[18][10][MAX_SUM][MAX_SUM];

int sum_of_digits(int n) {
    int sum = 0;
    while(n > 0) {
        sum += n%10;
        n /= 10;
    }
    return sum;
}


int main() {
    for(int i = 0 ; i <= 9; ++i)  {
        dp[0][i][i][sum_of_digits(137*i)] = 1;
    }

    std::vector<int> n137;

    for(int i = 0; i < 10; ++i) {
        n137.push_back(sum_of_digits(137*i));
    } 

    for(int i = 1 ; i < 18; ++i) {
        for(int digit = 0; digit <= 9; digit++ ) {
            for(int sum = 0; sum < MAX_SUM; sum++) {
                for(int sum137 = 0; sum137 < MAX_SUM; sum137++) {
                    for(int prev_digit = 0; prev_digit <= 9; prev_digit++) {
                        if(sum - digit >= 0 && sum137 - n137[digit] >= 0) {
                            dp[i][digit][sum][sum137] += dp[i-1][prev_digit][sum-digit][sum137-n137[digit]];
                        }
                    }
                }
            }
        }
    }

    int total = 0;
    for(int i = 0; i < 8; ++i) {
        for(int sum = 0; sum < MAX_SUM; sum++) {
            for(int digit = 1; digit <= 9; digit++) { 
                total += dp[i][digit][sum][sum];
            }
        }
    }

    std::cout << total << std::endl;

}