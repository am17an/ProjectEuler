#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

// Function to reverse a number
int64_t reverseNumber(int64_t num) {
    int64_t reversed = 0;
    while (num > 0) {
        reversed = reversed * 10 + (num % 10);
        num /= 10;
    }
    return reversed;
}

// Function to generate all palindromic numbers up to a given limit
std::vector<int64_t> generatePalindromes(int64_t limit) {
    std::vector<int64_t> palindromes;
    
    // Calculate the maximum number of digits based on the limit
    int maxDigits = floor(log10(limit)) + 1;
    
    // Add single-digit palindromes (0-9)
    for (int i = 0; i <= 9 && i <= limit; i++) {
        palindromes.push_back(i);
    }
    
    // Generate even-length palindromes
    for (int length = 2; length <= maxDigits; length += 2) {
        int halfLength = length / 2;
        int64_t start = pow(10, halfLength - 1);
        int64_t end = pow(10, halfLength) - 1;
        
        for (int64_t i = start; i <= end; i++) {
            int64_t reversed = reverseNumber(i);
            // For even-length palindromes, append the reverse to the original
            int64_t palindrome = i * pow(10, halfLength) + reversed;
            
            if (palindrome > limit) break;
            palindromes.push_back(palindrome);
        }
    }
    
    // Generate odd-length palindromes
    for (int length = 3; length <= maxDigits; length += 2) {
        int halfLength = length / 2;
        int64_t start = pow(10, halfLength - 1);
        int64_t end = pow(10, halfLength) - 1;
        
        for (int64_t i = start; i <= end; i++) {
            for (int mid = 0; mid <= 9; mid++) {
                // For odd-length palindromes, insert middle digit between original and reverse
                int64_t reversed = reverseNumber(i);
                int64_t palindrome = i * pow(10, halfLength + 1) + mid * pow(10, halfLength) + reversed;
                
                if (palindrome > limit) break;
                palindromes.push_back(palindrome);
            }
        }
    }
    
    // Sort the palindromes
    std::sort(palindromes.begin(), palindromes.end());
    
    return palindromes;
}

int main() {
    int64_t limit = 1e10; // Default limit of 10^10

    std::vector<int64_t> palindromes = generatePalindromes(limit);

    std::cout << palindromes.size() << std::endl;


    int64_t sq = 1;
    int64_t cu = 1;

    std::vector<int64_t> squares, cubes;

    while(sq * sq < limit) {
        squares.push_back(sq* sq);
        sq++;
    }

    while(cu * cu * cu < limit) {
        cubes.push_back(cu * cu * cu);
        cu++;
    }

    int64_t final_total = 0;
    int final_count = 0;
    for(int i = 0; i < palindromes.size(); i++) {

        int64_t palindrome = palindromes[i];
        int count = 0;
        for (int64_t cube: cubes) { 
            int64_t square = palindrome - cube;
            if(std::binary_search(squares.begin(), squares.end(), square)) {
                count++;
            }
            if(cube >= palindrome) break;
        }
        if(count == 4) {
            final_count++;
            final_total += palindrome;

            if(final_count == 5) {
                std::cout << final_total << std::endl;
                break;
            }
        }
    }
}