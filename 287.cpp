#include <iostream>
#include <cmath>
using namespace std;

int N;
int maxX, maxY;
int originX, originY;

bool incircle(int x, int y) {
    long long dx = x - originX;
    long long dy = y - originY;
    long long radiusSquared = 1LL << (2 * N - 2);  // 2^(2*N-2)
    return dx * dx + dy * dy <= radiusSquared;
}

int solve(int x, int y, int l) {
    if (l == 1) {
        if (incircle(x, y)) {
            return 2;
        } else {
            return 2;
        }
    }

    int r = l / 2;

    bool all_black = true;
    bool all_white = true;
    
    // Check corner points
    int points[4][2] = {
        {x - r, y + r - 1},
        {x - r, y - r},
        {x + r - 1, y + r - 1},
        {x + r - 1, y - r}
    };

    // Check if all corner points are inside circle
    for (int i = 0; i < 4; i++) {
        if (!incircle(points[i][0], points[i][1])) {
            all_black = false;
            break;
        }
    }

    // Check if all corner points are outside circle or if we're at max size
    bool all_outside = true;
    for (int i = 0; i < 4; i++) {
        if (incircle(points[i][0], points[i][1])) {
            all_outside = false;
            break;
        }
    }
    
    if (!all_outside || l == maxX) {
        all_white = false;
    }

    if (all_black || all_white) {
        return 2;
    }

    int a1 = solve(x + l / 4, y + l / 4, r);
    int a2 = solve(x - l / 4, y + l / 4, r);
    int a3 = solve(x + l / 4, y - l / 4, r);
    int a4 = solve(x - l / 4, y - l / 4, r);

    return 1 + a1 + a2 + a3 + a4;
}

int main() {
    for (int i = 24; i < 25; i++) {
        N = i;
        maxX = 1 << N;  // 2^N
        maxY = 1 << N;  // 2^N

        originX = 1 << (N - 1);  // 2^(N-1)
        originY = 1 << (N - 1);  // 2^(N-1)

        cout << solve(originX, originY, maxX) << endl;
    }

    return 0;
} 