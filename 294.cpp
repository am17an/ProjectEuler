#include <iostream>
#include <array>

int64_t dp[46][10][23][24];

std::array<int, 23> cycle = {
    10,8,11,18,19,6,14,2,20,16,22,13,15,12,5,4,17,9,21,3,7,1
};

int main() {

    for(int i = 0 ; i <= 9; ++i) {
        dp[0][i][i][i] = 1;
    }


    for(int step = 1; step < 46; step++) {
        for(int digit = 0; digit <= 9; ++digit) {
            for(int modulo = 0; modulo < 23; modulo++) {
                for(int sum = 0; sum <= 23; sum++) {
                    //dp[step][digit][modulo][sum]
                    //modulo 
                    int new_modulo = (cycle[(step-1)%23]*digit)%23;
                    for(int old_digit = 0; old_digit <= 9; ++old_digit) {
                        for(int old_modulo = 0 ; old_modulo < 23; old_modulo++) {
                            for(int old_sum = 0 ; old_sum <= 23 ; old_sum++) {
                                if((old_modulo + new_modulo)%23 == modulo && old_sum + digit == sum) {
                                    dp[step][digit][modulo][sum] += dp[step-1][old_digit][old_modulo][old_sum];
                                    //std::cout << "dp[" << step << "][" << digit << "][" << modulo << "][" << sum << "] += dp[" << step-1 << "][" << old_digit << "][" << old_modulo << "][" << old_sum << "]" << std::endl;
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    int64_t running_total = 0;
    for(int step = 1; step <= 45; step++) {
        int64_t total = 0;
        for(int digit = 1; digit<=9; ++digit) {
            running_total += dp[step][digit][0][23];
            total += dp[step][digit][0][23];
        }

        std::cout << "Step " << step << " total: " << total << " " << running_total%(1000000000) <<  std::endl;
    }

}