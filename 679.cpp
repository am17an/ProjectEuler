#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>

int64_t dp[31][4][4][4][(1<<4)];

std::vector<std::string> words = {"FREE", "FARE", "AREA", "REEF"};

std::unordered_map<int, std::string> charToIndex = {{0, "F"}, {1, "A"}, {2, "R"}, {3, "E"}};

int main() {
    for(int i = 0; i < 4; ++i) {
        for(int j = 0; j < 4; ++j) {
            for(int k = 0; k < 4; ++k) {
                dp[3][i][j][k][0] = 1;
            }
        }
    }

    for(int i = 4; i <= 30; ++i) {
        for(int j = 0; j < 4; ++j) {
            for(int k = 0; k < 4; ++k) {
                for(int l = 0; l < 4; ++l) {
                    for(int m = 0; m < (1<<4); ++m) {

                        for(int n = 0; n < 4; ++n) {
                            std::string word = charToIndex[n] + charToIndex[j] + charToIndex[k] + charToIndex[l];


                            if(auto it = std::find(words.begin(), words.end(), word); it != words.end()) {
                                int word_index = it - words.begin();

                               if(m & (1<<word_index)) {
                                  dp[i][n][j][k][m] += dp[i-1][j][k][l][m & ~(1<<word_index)];
                               } 
                            } else {
                                dp[i][n][j][k][m] += dp[i-1][j][k][l][m];
                            }
                        }
                    }
                }
            }
        }
    }

    int64_t ans = 0;
    for(int i = 0; i < 4; ++i) {
        for(int j = 0; j < 4; ++j) {
            for(int k = 0; k < 4; ++k) {
              ans += dp[30][i][j][k][(1<<4) - 1];
            }
        }
    }

    std::cout << ans << std::endl;
}
    
