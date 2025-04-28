#include <iostream>
#include <cstring>
int64_t matrix[2000][2000];
int64_t result[2000][2000];
int64_t mod = 20092010;
int64_t initial[2000];

void matrix_multiply(int64_t matrix1[2000][2000], int64_t matrix2[2000][2000]) {

    for(int i = 0 ; i < 2000; ++i) {
        for(int j = 0; j < 2000; ++j) {
            result[i][j] = 0;
            for(int k = 0; k < 2000; ++k) {
                result[i][j] += matrix2[i][k] * matrix2[k][j];
                result[i][j] %= mod;
            }
        }
    }

    memcpy(matrix1, result, sizeof(result));

}

void matrix_expo(int64_t matrix[2000][2000], int64_t n) {
    for(int i = 0; i < 2000; ++i) {
        for(int j = 0; j < 2000; ++j) {
            result[i][j] = matrix[i][j];
        }
    }

    while(n > 0) {
        std::cout << n << std::endl;
        if(n % 2 == 1) {
            matrix_multiply(result, matrix);
        }
        matrix_multiply(matrix, matrix);
        n /= 2;
    }
}

int main() {
    matrix[2000-1][0] = 1;
    matrix[2000-2][0] = 1;

    for(int row = 0; row + 1 < 2000; ++row) {
       matrix[row][row+1] = 1;
    }

    matrix_expo(matrix, 20000);


    int64_t ans = 0;
    for(int i = 0; i < 2000; ++i) {
        ans += matrix[0][i];
        ans %= mod;
    }

    std::cout << ans << std::endl;
}