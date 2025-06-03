#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

const long long MOD = 1000000000;  // 10^9, not 10^9+7
const long long n = 1234567898765LL;
const int k = 4321;

// Function to multiply two matrices with modular arithmetic
vector<vector<long long>> matmul(const vector<vector<long long>>& A, const vector<vector<long long>>& B) {
    int rows = A.size();
    int cols = B[0].size();
    int common = A[0].size();
    
    vector<vector<long long>> result(rows, vector<long long>(cols, 0));
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            for (int k = 0; k < common; k++) {
                result[i][j] += A[i][k] * B[k][j];
            }
            result[i][j] %= MOD;
        }
    }
    
    return result;
}

// Matrix exponentiation with modular arithmetic
vector<vector<long long>> matrix_power(vector<vector<long long>> M, long long exp) {
    int size = M.size();
    vector<vector<long long>> result(size, vector<long long>(size, 0));
    
    // Initialize identity matrix
    for (int i = 0; i < size; i++) {
        result[i][i] = 1;
    }
    
    while (exp > 0) {
        if (exp & 1) {
            result = matmul(result, M);
        }
        M = matmul(M, M);
        std::cout << "Done 1 mat mul" << std::endl;
        exp >>= 1;
    }
    
    return result;
}

int main() {
    // Find divisors of n
    vector<long long> digits;
    for (long long i = 1; i * i <= n; i++) {
        if (n % i == 0) {
            digits.push_back(i);
            if (i != n / i) {
                digits.push_back(n / i);
            }
        }
    }
    
    cout << "Number of divisors: " << digits.size() << endl;
    
    // Create transition matrix
    vector<vector<long long>> matrix(k, vector<long long>(k, 0));
    
    for (int i = 0; i < k; i++) {
        for (long long dig : digits) {
            int new_mod = (i + dig) % k;
            matrix[new_mod][i] = 1;
        }
    }
    
    // Compute matrix^n
    vector<vector<long long>> result_matrix = matrix_power(matrix, n);
    
    // Initial state vector (we start at position n % k)
    vector<long long> initial(k, 0);
    initial[n % k] = 1;
    
    // We only need the first row of result_matrix @ initial
    // This is just the dot product of result_matrix[0] with initial
    long long answer = result_matrix[0][n % k] % MOD;
    
    cout << "Answer: " << answer << endl;
    
    return 0;
} 