#include <iostream>
#include <map>
#include <vector>

const int N = 4;

std::map<int, int64_t> memo;
int64_t MOD = 987654319;

int64_t solve(int N) {

    if(N <= 1) {
        return 1;
    }

    if(memo.find(N) != memo.end()) {
        return memo[N];
    }

    int64_t ans = 0;

    for(int i = 0; i < N ; ++i) {
        int group1 = i;
        int group2 = N - i - 1;

        int g1 = 1;
        int g2 = 1;

        if(group1 > 0) {
            g1 = solve(group1);
        }
        if(group2 > 0) {
            g2 = solve(group2);
        }

        int64_t prob = ((2*N-1));

        ans += (prob*g1%MOD*g2%MOD)%MOD;
        ans %= MOD;
    }

    memo[N] = ans%MOD;
    return ans;
}

int main() {
    std::cout << solve(100) << std::endl;
}
