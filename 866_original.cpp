#include <iostream>
#include <map>
#include <vector>

using State = std::pair<std::map<int, int>, int>;

const int N = 4;

std::map<State, int64_t> memo;

int64_t solve(State const & S) {

    auto const & pieces = S.first;
    int done = S.second;

    if(done == N) {
        return 1;
    }

    if(memo.find(S) != memo.end()) {
        return memo[S];
    }

    int64_t ans = 0;
    for(auto & [piece, count]: pieces) {
        std::cout << "Step " << done << ", Piece " << piece << "," << count << std::endl;

        for(int i = 0; i < piece; ++i) {
            std::map<int, int> newM =  pieces;

            int group1 = i;
            int group2 = piece - i - 1;

            newM[piece] -- ;
            if(newM[piece] == 0) {
                newM.erase(piece);
            }

            if(group1 > 0) {
                newM[group1]++;
            }

            if(group2 > 0) {
                newM[group2]++;
            }

            int64_t prob = (piece*(2*piece-1));
            State newS;
            newS.first = std::move(newM);
            newS.second = done+1;

            std::cout << "  Breaking at " << i << " -> (" << group1 << "," << group2 
                      << "), prob=" << prob << ", factor=" << count << std::endl;

            ans += (prob*count*solve(newS))/(N-done);
            ans %= 987654319;
        }
    }

    memo[S] = ans;
    return ans;
}

int main() {
    State s;
    std::map<int, int> mp;
    mp[N] = 1;
    s.first = mp;
    s.second = 0;
    std::cout << solve(s) << std::endl;
} 