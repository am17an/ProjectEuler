#include <iostream>
#include <vector>
#include <unordered_map>
#include <cassert>

using namespace std;

class TowerTilingDP {
private:
    int N;
    unordered_map<int, long long> dp[2];
    
    // Check if position (x,y) is valid in a 3x3 grid
    bool isValid(int x, int y) {
        return x >= 0 && x < 3 && y >= 0 && y < 3;
    }
    
    // Convert (x,y) to bit position in mask
    int toBit(int x, int y) {
        return x * 3 + y;
    }
    
    // Check if bit is set in mask
    bool isSet(int mask, int x, int y) {
        return mask & (1 << toBit(x, y));
    }
    
    // Set bit in mask
    int setBit(int mask, int x, int y) {
        return mask | (1 << toBit(x, y));
    }
    
    // Fill current layer and generate next layer states
    void fill(int pos, int curMask, int nextMask, int layer, long long ways) {
        if (pos == 9) {
            // Finished processing this layer
            dp[(layer + 1) & 1][nextMask] += ways;
            return;
        }
        
        int x = pos / 3, y = pos % 3;
        
        if (isSet(curMask, x, y)) {
            // This position is already filled, move to next
            fill(pos + 1, curMask, nextMask, layer, ways);
            return;
        }
        
        // Try placing blocks in different orientations
        
        // 1. Place block horizontally (along y-axis): (x,y) and (x,y+1)
        if (isValid(x, y + 1) && !isSet(curMask, x, y + 1)) {
            int newCurMask = setBit(setBit(curMask, x, y), x, y + 1);
            fill(pos + 1, newCurMask, nextMask, layer, ways);
        }
        
        // 2. Place block vertically (along x-axis): (x,y) and (x+1,y)
        if (isValid(x + 1, y) && !isSet(curMask, x + 1, y)) {
            int newCurMask = setBit(setBit(curMask, x, y), x + 1, y);
            fill(pos + 1, newCurMask, nextMask, layer, ways);
        }
        
        // 3. Place block along z-axis: (x,y) in current layer and (x,y) in next layer
        if (layer + 1 < N) {
            int newCurMask = setBit(curMask, x, y);
            int newNextMask = setBit(nextMask, x, y);
            fill(pos + 1, newCurMask, newNextMask, layer, ways);
        }
    }
    
public:
    TowerTilingDP(int n) : N(n) {
        dp[0].clear();
        dp[1].clear();
    }
    
    long long solve() {
        if (N == 0) return 1;
        
        // Initialize: empty first layer
        dp[0][0] = 1;
        
        for (int layer = 0; layer < N; layer++) {
            dp[(layer + 1) & 1].clear();
            
            for (auto& state : dp[layer & 1]) {
                int mask = state.first;
                long long ways = state.second;
                
                if (ways > 0) {
                    fill(0, mask, 0, layer, ways);
                }
            }
        }
        
        // Answer is the number of ways to reach the final layer with empty state
        return dp[N & 1][0];
    }
};

int main() {
    cout << "Computing values using bitmask DP..." << endl;
    
    // Compute initial values for the recurrence relation
    vector<long long> values;
    
    for (int i = 0; i <= 25; i++) {
        TowerTilingDP solver(i);
        long long result = solver.solve();
        values.push_back(result);
        cout << "a(" << i << ") = " << result << endl;
    }
    
    return 0;
}
