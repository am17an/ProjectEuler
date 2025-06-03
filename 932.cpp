#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>

std::vector<int64_t> squares;

bool is_2025_number(int64_t num) {

    std::vector<int32_t> digits;
    int64_t temp = num;
    while(temp > 0) {
        digits.push_back(temp % 10);
        temp /= 10;
    }

    //if any of the splits of digits, from non-zero digits is equal to num, return true

    int64_t num2 = num/10;
    //std::reverse(digits.begin(), digits.end());
    int64_t current_num = digits[0];

    for(int i = 1 ; i < digits.size(); ++i) {
        int64_t sq = current_num + num2;

        if(digits[i] == 0) continue;

        if(sq*sq == num and current_num != 0) {
            std::cout << "sq " << num2 << " " << current_num << " " << sq*sq << std::endl;
            return true;
        }

        // Replace pow with integer multiplication to avoid floating-point precision issues
        int64_t power_of_ten = 1;
        for (int j = 0; j < i; j++) {
            power_of_ten *= 10;
        }
        current_num = digits[i] * power_of_ten + current_num;
        
        num2 /= 10;
    }

    return false;
}

int main() {
    // Replace floating-point literal with integer literal to avoid precision issues
    int64_t limit = 10000000000000000; // 10^16
    for(int64_t i = 1; i*i <= limit; i++) {
        squares.push_back(i*i);
    }

    //std::cout << is_2025_number(3025) << std::endl;
    //std::cout << is_2025_number(981) << std::endl;
    //std::cout << is_2025_number(2025) << std::endl;

    int64_t count = 0;
    for(int64_t i = 0; i < squares.size(); i++) {
        if(is_2025_number(squares[i])) {
            std::cout << "Is 2025 " << squares[i] << std::endl;
            count += squares[i];
        }
    }

    std::cout << count << std::endl;
}